namespace DefaultNamespace;

public class WebhookPayload
{
    public string EventType { get; set; } = string.Empty;
    public object Data { get; set; } = new();
}