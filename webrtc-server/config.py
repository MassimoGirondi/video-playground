import os 
import inspect
import sys
from pathlib import Path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, str(Path(parentdir) / "transformers"))

from video_transformer import VideoTransformTrack
import openrtist_transformer
import edge_transformer
import empty_transformer


models = {
    'mosaic': { 'class': openrtist_transformer.OpenrtistTransformer,
                'args': {'model_name' : 'mosaic'},
                'description': "Openrtist Mosaic", 
               },
    'passthrough' : {'class': empty_transformer.EmptyTransformer,
                     'description': "Passthrough", 
                     'default' : True,
                     },
    'edges' : {'class': edge_transformer.EdgeTransformer,
                     'description': "Edge detection", 
                     },
    'monet' : { 'class': openrtist_transformer.OpenrtistTransformer,
                'args': {'model_name' : 'monet'},
                'description': "Openrtist Monet", 
               },

}
        # if transform == "edges":
        #     self.transformer = edge_transformer.EdgeTransformer()
        # elif transform in ["mosaic", "cafe_gogh", "sunday_afternoon"]:
        #     self.transformer = openrtist_transformer.OpenrtistTransformer(transform, device=device)
        # elif transform in ["ninasr_b0"]:
        #     self.transformer = superresolution_transformer.SuperresolutionTransformer(transform, device=device)
        # elif transform == "dummy":
        #     self.transformer = dummy_transformer.DummyTransformer(device = "cuda")
        # elif transform == "dummy-cpu":
        #     self.transformer = dummy_transformer.DummyTransformer()
        # elif transform == "dummy-nothing":
        #     self.transformer = dummy_transformer.DummyTransformer(do_nothing=True)
        # elif "rdma-" in transform:
        #     self.transformer = rdma_transformer.RDMATransformer(model="nothing")
        # else:



def models_select():
    s = "<select id='video-transform'>\n"
    for k,v in models.items():
        default = "selected" if "default" in v else ""
        s+=f"<option value='{k}' {default}>{v['description']}</option>\n"
    s+= "</select>\n"
    return s


