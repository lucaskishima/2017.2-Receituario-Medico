# Django
from django.views.generic import DetailView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Local Django
from prescription.models import (Prescription,
                                 PrescriptionHasMedicine,
                                 PrescriptionHasManipulatedMedicine,
                                 )
from user.decorators import is_health_professional
from prescription import constants


class ShowDetailPrescriptionView(DetailView):
    """
    Print done prescription.
    """
    template_name = 'show_detail_prescription.html'
    context_object_name = 'form_medicine'

    @method_decorator(login_required)
    @method_decorator(is_health_professional)
    def dispatch(self, *args, **kwargs):
        return super(ShowDetailPrescriptionView, self).dispatch(*args, **kwargs)

    # Return a JSON's prescription.
    def get(self, request, *args, **kwargs):
        data = dict()

        prescription = self.get_context(request)
        prescription_medicine = self.get_has_medicine(prescription)
        prescription_manipulated_medicine = self.get_has_manipulated_medicine(prescription)

        for medicine in prescription_medicine:
            medicine.quantity = constants.QUANTITY_CHOICES[medicine.quantity][1]

        for medicine in prescription_manipulated_medicine:
            medicine.quantity = constants.QUANTITY_CHOICES[medicine.quantity][1]

        context = {
            'prescription': prescription,
            'prescription_medicine': prescription_medicine,
            'prescription_manipulated_medicine': prescription_manipulated_medicine,
            }

        data['html_form'] = render_to_string(self.template_name, context, request=request)
        # Json to communication Ajax.
        return JsonResponse(data)

    # Get a Prescription object in database.
    def get_context(self, request):
        pk = self.kwargs['pk']
        return Prescription.objects.get(pk=pk)

    def get_has_medicine(self, prescription):
        return PrescriptionHasMedicine.objects.filter(prescription_medicine=prescription)

    def get_has_manipulated_medicine(self, prescription):
        return PrescriptionHasManipulatedMedicine.objects.filter(prescription_medicine=prescription)