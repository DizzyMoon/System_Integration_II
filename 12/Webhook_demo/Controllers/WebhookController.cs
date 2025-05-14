using DefaultNamespace;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class WebhookController : ControllerBase
{
    private readonly WebhookDbContext _context;

    public WebhookController(WebhookDbContext context)
    {
        _context = context;
    }
    
    [HttpPost("simulate-user-created")]
    public async Task<IActionResult> SimulateUserCreated([FromServices] WebhookTriggerService webhookService)
    {
        var fakeUser = new
        {
            Id = 123,
            Email = "test@example.com",
            Name = "Test User"
        };

        await webhookService.TriggerWebhooksAsync("user.created", fakeUser);

        return Ok("Webhook triggered");
    }


    [HttpPost("register")]
    public async Task<IActionResult> RegisterWebhook([FromBody] WebhookRegistration registration)
    {
        registration.CreatedAt = DateTime.UtcNow;
        _context.WebhookRegistrations.Add(registration);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetWebhook), new { id = registration.Id }, registration);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetWebhook(int id)
    {
        var webhook = await _context.WebhookRegistrations.FindAsync(id);
        if (webhook == null)
        {
            return NotFound();
        }
        return Ok(webhook);
    }
}