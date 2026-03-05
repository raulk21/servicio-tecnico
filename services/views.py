from django.shortcuts import render,  get_object_or_404, redirect
from .models import Service, ContactRequest
from .forms import ContactRequestForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage


def home(request):
    services = Service.objects.all()
    return render(request, 'services/home.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ContactRequestForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.service = service
            contact.save()
            print(settings.EMAIL_HOST_USER)
            send_mail(
            subject=f"Confirmación de orden {contact.order_number} fue registrada",
            message=f"""
            Hola {contact.name},

                Tu solicitud fue recibida correctamente.

                Número de orden: {contact.order_number}
                Servicio: {contact.service.title}
                Estado actual: Pendiente

                Gracias por confiar en nuestro servicio técnico.
                """,
            #from_email="servicio@taller.com",
            
            from_email=f"Servicio Técnico <{settings.EMAIL_HOST_USER}>",
            recipient_list=[contact.email],
            fail_silently=False,     
            )

            # correo para tu negocio
            email = EmailMessage(
                subject=f"Nueva orden {contact.order_number}",
                body=f"""
            Nueva orden recibida

            Número de orden: {contact.order_number}

            Nombre: {contact.name}
            Teléfono: {contact.phone}
            Email: {contact.email}

            Mensaje del cliente:
            {contact.message}
            """,
                from_email=settings.EMAIL_HOST_USER,
                to=["servicio.tecnico.elect21@gmail.com"],
            )
            if contact.image:
                email.attach_file(contact.image.path)

            email.send(fail_silently=False)

            return redirect('request_success', request_id=contact.id)
    else:
        form = ContactRequestForm()

    return render(request, 'services/service_detail.html', {
        'service': service,
        'form': form
    })

def request_success(request, request_id):
    contact = ContactRequest.objects.get(id=request_id)
    return render(request, 'services/request_success.html', {
        'contact': contact
    }) 

def track_order(request):
    order = None
    error = None

    if request.method == "POST":
        order_number = request.POST.get("order_number")

        try:
            order = ContactRequest.objects.get(order_number=order_number)
        except ContactRequest.DoesNotExist:
            error = "Orden no encontrada"

    return render(request, "services/track_order.html", {
        "order": order,
        "error": error
    })


from django.shortcuts import render
from .models import ContactRequest

def check_order(request):
    order = None
    error = None

    if request.method == "POST":
        order_number = request.POST.get("order_number")

        try:
            order = ContactRequest.objects.get(order_number=order_number)
        except ContactRequest.DoesNotExist:
            error = "Orden no encontrada"

    return render(request, "services/check_order.html", {
        "order": order,
        "error": error
    })
# Create your views here.
