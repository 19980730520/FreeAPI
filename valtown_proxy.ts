export default async function(req: Request): Promise<Response> {
    const url = new URL(req.url);
    const path = url.pathname;
  
    // Add CORS headers for cross-origin requests
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
  
    // Handle OPTIONS preflight requests
    if (req.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders,
      });
    }
  
    // New AI proxy endpoint
    switch (path) {
      case "/api/ai-proxy":
        if (req.method !== "POST") {
          return new Response("Only POST method is allowed", {
            status: 405,
            headers: corsHeaders,
          });
        }
  
        try {
          // Parse incoming JSON
          const { prompt, image } = await req.json();
  
          // Validate input
          if (!prompt) {
            return new Response("Prompt is required", {
              status: 400,
              headers: corsHeaders,
            });
          }
  
          // Dynamically import OpenAI to ensure server-side execution
          const { OpenAI } = await import("https://esm.town/v/std/openai");
          const openai = new OpenAI();
  
          // Prepare messages for OpenAI
          const messages: any[] = [{
            role: "user",
            content: [
              { type: "text", text: prompt },
            ],
          }];
  
          // Add image if base64 is provided
          if (image) {
            messages[0].content.push({
              type: "image_url",
              image_url: { url: image },
            });
          }
  
          // Call OpenAI API
          const response = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: messages,
            max_tokens: 300,
          });
  
          // Return AI response
          return Response.json({
            response: response.choices[0].message.content,
            timestamp: new Date().toISOString(),
          }, {
            headers: {
              ...corsHeaders,
              "Content-Type": "application/json",
            },
          });
        } catch (error) {
          console.error("AI Proxy Error:", error);
          return new Response(
            JSON.stringify({
              error: "Failed to process request",
              details: error.message,
            }),
            {
              status: 500,
              headers: {
                ...corsHeaders,
                "Content-Type": "application/json",
              },
            },
          );
        }
  
      default:
        return Response.json({
          message: "Welcome to the API! 🚀",
          available_endpoints: ["/api/ai-proxy"],
        }, { status: 200 });
    }
  }