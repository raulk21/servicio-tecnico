from django.shortcuts import render,  get_object_or_404, redirect
from .models import Service, ContactRequest
from .forms import ContactRequestForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q



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

def client_panel(request):
    email = request.GET.get("email")
    orders = ContactRequest.objects.none()

    if email:
        orders = ContactRequest.objects.filter(email=email).order_by("-created_at")

    return render(request, "services/client_panel.html", {
        "orders": orders,
        "email": email
    })

def order_detail(request, order_number):
    order = get_object_or_404(ContactRequest, order_number=order_number)

    return render(request, "services/order_detail.html", {
        "order": order
    })

@staff_member_required
def update_order_status(request, order_id, new_status):
    
    order = ContactRequest.objects.get(id=order_id)
    order.status = new_status
    order.save()

    return redirect("order_detail", order_number=order.order_number)

def workshop_panel(request):

    buscar = request.GET.get("buscar")
    status = request.GET.get("status")
    orders = ContactRequest.objects.all()

    # filtro por texto
    if buscar:
        orders = orders.filter(
            Q(name__icontains=buscar) |
            Q(id__startswith=buscar)
        )

    if status:
        orders = orders.filter(status=status)

    orders = orders.order_by("-created_at")

    pendientes = ContactRequest.objects.filter(status="pendiente").count()
    diagnostico = ContactRequest.objects.filter(status="diagnostico").count()
    proceso = ContactRequest.objects.filter(status="proceso").count()
    espera = ContactRequest.objects.filter(status="espera").count()
    finalizado = ContactRequest.objects.filter(status="finalizado").count()

    return render(request, "services/workshop_panel.html", {
        "orders": orders,
        "pendientes": pendientes,
        "diagnostico": diagnostico,
        "proceso": proceso,
        "espera": espera,
        "finalizado": finalizado
    })

def update_order(request, order_id):

    order = get_object_or_404(ContactRequest, id=order_id)

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.diagnostic = request.POST.get("diagnostic")
        order.repair_cost = request.POST.get("repair_cost")

        order.save()

    return render(request, "services/order_detail.html", {
        "order": order
    })   
# Create your views here.
