from django import forms
from event.models import Event, Category

class StyledFormMixin:
    default_classes = "w-full px-3 py-2 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-3"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
           
                if field_name == "location":
                    field.widget.attrs.update({
                        "class": self.default_classes,
                        "placeholder": "Enter location : "
                    })
                else:
                    field.widget.attrs.update({
                        "class": self.default_classes,
                        "placeholder": f"Enter {field.label.lower()}"
                    })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "w-1/6 px-3 py-2 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-3"
                })
                
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "type": "time",
                    "class": "border border-gray-300 w-18 p-2 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 cursor-pointer"
                })
                
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2 mt-2 ml-2"
                })
                
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.default_classes
                })
                
            else:
                field.widget.attrs.update({
                    "class": "w-full px-3 py-2 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-3"
                })

class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            "date": forms.SelectDateWidget,
            "time": forms.TimeInput(attrs={"type": "time"}),
            "participants": forms.CheckboxSelectMultiple
            
        }
        
        labels = {
            "time": "Event Time (HH:MM:AM/PM)",
            "location": "Location (Just enter the city name)"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Select category"
        self.apply_styled_widgets()
        
        
        
        
class CategoryModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
        
