export async function fetchUtil(
  path: string,
  body?: BodyInit,
  method?: string,
): Promise<Response> {
  if (!method) {
    method = body ? 'POST' : 'GET';
  }

  return fetch(import.meta.env.VUE_APP_API_PREFIX + path, {
    body,
    headers: {
      'Content-Type': 'application/json',
    },
    method,
    redirect: 'follow',
  });
}
