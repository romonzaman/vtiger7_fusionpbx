
def get_header(event, header_name):
    try:
        hdr = event.getHeader(header_name)
        if hdr:
            return hdr
        else:
            return ""
    except:
        return ""