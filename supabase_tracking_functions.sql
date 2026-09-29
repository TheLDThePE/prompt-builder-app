-- Run this in Supabase SQL Editor after the app_users and activity_events
-- tables have been created. The app calls these functions using the server-side
-- service_role key; no prompt text is stored.

-- Add a unique event identifier so Streamlit reruns/retries cannot double-count
-- one browser copy action. Existing rows remain valid with NULL identifiers.
alter table public.activity_events
    add column if not exists client_event_id uuid;

create unique index if not exists activity_events_client_event_id_uidx
    on public.activity_events (client_event_id);

-- Record one app session/login. first_login_at is preserved on later visits.
create or replace function public.record_app_login(
    p_google_sub text,
    p_email text
)
returns void
language sql
security invoker
set search_path = public
as $$
    insert into public.app_users (
        google_sub,
        email,
        first_login_at,
        last_login_at,
        login_count,
        prompt_copy_count
    )
    values (
        p_google_sub,
        p_email,
        now(),
        now(),
        1,
        0
    )
    on conflict (google_sub) do update
    set email = excluded.email,
        last_login_at = now(),
        login_count = app_users.login_count + 1;
$$;

-- Store one copy action and increment the per-user counter atomically.
create or replace function public.record_prompt_copy(
    p_google_sub text,
    p_client_event_id uuid
)
returns void
language plpgsql
security invoker
set search_path = public
as $$
begin
    insert into public.activity_events (
        google_sub,
        event_type,
        occurred_at,
        client_event_id
    )
    values (
        p_google_sub,
        'copy_prompt',
        now(),
        p_client_event_id
    )
    on conflict (client_event_id) do nothing;

    if found then
        update public.app_users
        set prompt_copy_count = prompt_copy_count + 1
        where google_sub = p_google_sub;
    end if;
end;
$$;

-- Keep these procedures unavailable to public/anonymous/authenticated browser
-- clients. The server-side service_role can execute them.
revoke all on function public.record_app_login(text, text)
    from public, anon, authenticated;
grant execute on function public.record_app_login(text, text)
    to service_role;

revoke all on function public.record_prompt_copy(text, uuid)
    from public, anon, authenticated;
grant execute on function public.record_prompt_copy(text, uuid)
    to service_role;
