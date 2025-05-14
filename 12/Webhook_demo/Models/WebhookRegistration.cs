using System;
namespace DefaultNamespace;
public class WebhookRegistration
{
    public int Id { get; set; }
    public string EventType { get; set; } = string.Empty;
    public string TargetUrl { get; set; } = string.Empty;
    public string Secret { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
}