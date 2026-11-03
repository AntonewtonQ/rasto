import type { NextConfig } from "next";

// O Django serve a API e a autenticação. Em desenvolvimento, o Next.js encaminha /api e /_allauth para ele,
// para o navegador ver uma só origem (cookies de sessão e CSRF). Em produção o Caddy faz o mesmo encaminhamento.
const DJANGO = process.env.DJANGO_INTERNO ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  // Modelo de cache anterior (sem Cache Components): as páginas são autenticadas e dinâmicas; ver DECISOES.md.
  cacheComponents: false,
  poweredByHeader: false,
  output: "standalone", // imagem Docker pequena (frontend/Dockerfile)
  async rewrites() {
    return [
      { source: "/api/:caminho*", destination: `${DJANGO}/api/:caminho*` },
      { source: "/_allauth/:caminho*", destination: `${DJANGO}/_allauth/:caminho*` },
    ];
  },
  async headers() {
    return [
      {
        source: "/:caminho*",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
        ],
      },
    ];
  },
};

export default nextConfig;
