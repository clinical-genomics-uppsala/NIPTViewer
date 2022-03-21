from niptviewer import __version__


def niptviewer_version(request):
    return {
        'niptviewer_version': __version__,
    }
