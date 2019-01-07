from Venter.models import Organisation, Category
from Backend import settings

cat_list = settings.ICMC_CATEGORY_LIST
org_name = Organisation.objects.get(organisation_name='ICMC')
for x in cat_list:
    Category.objects.create(organisation=org_name, category=x)    
