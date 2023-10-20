Bun.serve({
  fetch(req) {
    const urlPath = new URL(req.url).pathname;

    if (urlPath.endsWith(".css")) {
      return new Response(Bun.file(`.${urlPath}`), {
        headers: { "Content-Type": "text/css" },
      });
    }

    if (urlPath.endsWith(".js")) {
      return new Response(Bun.file(`.${urlPath}`), {
        headers: { "Content-Type": "text/javascript" },
      });
    }

    return new Response(Bun.file("index.html"), {
      headers: { "Content-Type": "text/html" },
    });
  },
  error(error) {
    console.error(error);
    throw new Error("Check Path.");
  },
});
