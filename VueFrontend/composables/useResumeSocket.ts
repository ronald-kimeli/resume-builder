/**
 * Live resume updates from the Node socket server (/ws/user/{id}), fed by RabbitMQ.
 * FastAPI publishes `{ event: 'resume.updated', ... }` whenever any of the user's
 * resume sections change, so open previews/forms can refetch instead of polling.
 */
export const useResumeSocket = (
  userId: MaybeRefOrGetter<number | string | null | undefined>,
  onUpdate: (message: Record<string, any>) => void,
) => {
  const { public: { SOCKET_URL } } = useRuntimeConfig();
  const connected = ref(false);

  let socket: WebSocket | null = null;
  let retryTimer: ReturnType<typeof setTimeout> | undefined;
  let heartbeat: ReturnType<typeof setInterval> | undefined;
  let retries = 0;
  let closedByUs = false;

  // SOCKET_URL looks like ws://localhost:4000 -> ws://localhost:4000/ws/user/{id}
  const socketUrl = (id: number | string) =>
    `${(SOCKET_URL as string).replace(/\/$/, '')}/ws/user/${id}`;

  const cleanup = () => {
    clearInterval(heartbeat);
    clearTimeout(retryTimer);
  };

  const connect = () => {
    const id = toValue(userId);
    if (!import.meta.client || !id) return;
    closedByUs = false;
    socket = new WebSocket(socketUrl(id));

    socket.onopen = () => {
      connected.value = true;
      retries = 0;
      heartbeat = setInterval(() => socket?.send('ping'), 25_000);
    };
    socket.onmessage = (e) => {
      const message = JSON.parse(e.data);
      if (message.event !== 'pong') onUpdate(message);
    };
    socket.onclose = () => {
      connected.value = false;
      cleanup();
      if (closedByUs) return;
      // exponential backoff, capped at 30s
      retryTimer = setTimeout(connect, Math.min(1000 * 2 ** retries++, 30_000));
    };
  };

  const close = () => {
    closedByUs = true;
    cleanup();
    socket?.close();
  };

  onMounted(connect);
  onBeforeUnmount(close);
  watch(() => toValue(userId), () => { close(); connect(); });

  return { connected, close };
};
