using System.Net.Http.Json;
using DefaultNamespace;
using Microsoft.EntityFrameworkCore;

public class WebhookTriggerService
{
    private readonly WebhookDbContext _context;
    private readonly IHttpClientFactory _httpClientFactory;

    public WebhookTriggerService(WebhookDbContext context, IHttpClientFactory httpClientFactory)
    {
        _context = context;
        _httpClientFactory = httpClientFactory;
    }

    public async Task TriggerWebhooksAsync(string eventType, object payload)
    {
        var hooks = await _context.WebhookRegistrations
            .Where(w => w.EventType == eventType)
            .ToListAsync();

        var client = _httpClientFactory.CreateClient();

        foreach (var hook in hooks)
        {
            var requestPayload = new WebhookPayload
            {
                EventType = eventType,
                Data = payload
            };

            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, hook.TargetUrl)
                {
                    Content = JsonContent.Create(requestPayload)
                };

                request.Headers.Add("X-Webhook-Secret", hook.Secret);

                var response = await client.SendAsync(request);
                response.EnsureSuccessStatusCode(); // throw if not 2xx
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to trigger webhook: {ex.Message}");
                // Optionally log or retry failed calls
            }
        }
    }
}