import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL =
  process.env.AGENTOPS_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

async function proxy(request: NextRequest, path: string[]) {
  const targetPath = path.join("/");
  const targetUrl = new URL(`${API_BASE_URL}/${targetPath}`);

  request.nextUrl.searchParams.forEach((value, key) => {
    targetUrl.searchParams.append(key, value);
  });

  try {
    const response = await fetch(targetUrl, {
      method: request.method,
      headers: {
        "content-type": request.headers.get("content-type") || "application/json",
      },
      body: request.method === "GET" || request.method === "HEAD"
        ? undefined
        : await request.text(),
    });

    return new NextResponse(response.body, {
      status: response.status,
      headers: {
        "content-type": response.headers.get("content-type") || "application/json",
      },
    });
  } catch {
    return NextResponse.json(
      {
        detail: "Backend unavailable",
      },
      { status: 502 }
    );
  }
}

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params;
  return proxy(request, path);
}

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params;
  return proxy(request, path);
}
