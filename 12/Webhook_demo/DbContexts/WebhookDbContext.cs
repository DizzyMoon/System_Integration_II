using DefaultNamespace;
using Microsoft.EntityFrameworkCore;

public class WebhookDbContext : DbContext
{
    public DbSet<WebhookRegistration> WebhookRegistrations { get; set; }

    public WebhookDbContext(DbContextOptions<WebhookDbContext> options)
        : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<WebhookRegistration>().ToTable("webhook_registrations");
        modelBuilder.Entity<WebhookRegistration>().Property(w => w.Id).HasColumnName("id");
        modelBuilder.Entity<WebhookRegistration>().Property(w => w.EventType).HasColumnName("event_type");
        modelBuilder.Entity<WebhookRegistration>().Property(w => w.TargetUrl).HasColumnName("target_url");
        modelBuilder.Entity<WebhookRegistration>().Property(w => w.Secret).HasColumnName("secret");
        modelBuilder.Entity<WebhookRegistration>().Property(w => w.CreatedAt).HasColumnName("created_at");
    }
}