def setup():
    from glue.config import qt_client
    from .glue_viewer import GlueVTKViewer
    qt_client.add(GlueVTKViewer)
