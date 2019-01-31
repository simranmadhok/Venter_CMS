from Venter.models import Header

def csv_file_header_validation(uploaded_csv_file, request):
    # extracting and converting the header from bytes to string format
    csv_header = uploaded_csv_file.readline()
    csv_str = str(csv_header, encoding='utf-8')

    # converting the headers from string to list using comma separated delimiters
    csv_list = csv_str.split(',')

    # strip() function executes over each item of csv_list to remove all the leading and trailing whitespaces
    # this should normalise all the header categories with whitespaces in them
    # then we cast the list to a set to allow us to validate it with the organisation's header list
    csv_striped_list = [item.strip() for item in csv_list]
    csv_set = set(csv_striped_list)

    # obtaining the organisation name of the logged in user
    # this retrieves the header list for a particular organisation and casts it to a set
    org_name = request.user.profile.organisation_name
    model_header_list = Header.objects.filter(
        organisation_name=org_name).values_list('header', flat=True)
    header_set = set(model_header_list)
    if csv_set == header_set:
        return True
    return False
