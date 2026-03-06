from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_time = models.CharField(max_length=100, blank=True)
    reference_price = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='services_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ContactRequest(models.Model):

    STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('diagnostico', 'En diagnóstico'),
    ('proceso', 'En reparación'),
    ('espera', 'Esperando repuesto'),
    ('finalizado', 'Finalizado'),
]

    order_number = models.CharField(max_length=20, unique=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='contact_images/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendiente'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.order_number} - {self.name}"

    def save(self, *args, **kwargs):

    # Detectar si es actualización
        if self.pk:
            old = ContactRequest.objects.get(pk=self.pk)

            if old.status != self.status:
                 send_mail(
                subject=f"Actualización de tu orden {self.order_number}",
                message=f"""
    Hola {self.name},

    El estado de tu orden {self.order_number} cambió.

    Nuevo estado: {self.get_status_display()}

    Gracias por confiar en nuestro servicio técnico.
    """,
    from_email="servicio@taller.com",
    recipient_list=[self.email],
    fail_silently=False,
    )

    # Generar número de orden si no existe
        if not self.order_number:
            year = timezone.now().year
            last_order = ContactRequest.objects.filter(
                order_number__startswith=f"OT-{year}"
        ).count() + 1

            self.order_number = f"OT-{year}-{last_order:04d}"

        super().save(*args, **kwargs)
    
class RepairUpdate(models.Model):

    order = models.ForeignKey(ContactRequest, on_delete=models.CASCADE, related_name="updates")
    status = models.CharField(max_length=50)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.status}"