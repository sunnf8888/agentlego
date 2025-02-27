from typing import Callable, Union

from agentlego.parsers import DefaultParser
from agentlego.schema import ToolMeta
from agentlego.types import ImageIO
from agentlego.utils import require
from ..base import BaseTool
from ..utils.diffusers import load_sd, load_sdxl


class DepthTextToImage(BaseTool):
    """A tool to generate image according to a depth image.

    Args:
        toolmeta (dict | ToolMeta): The meta info of the tool. Defaults to
            the :attr:`DEFAULT_TOOLMETA`.
        parser (Callable): The parser constructor, Defaults to
            :class:`DefaultParser`.
        model (str): The depth controlnet model to use. You can choose
            from "sd" and "sdxl". Defaults to "sd".
        device (str): The device to load the model. Defaults to 'cuda'.
    """

    DEFAULT_TOOLMETA = ToolMeta(
        name='DepthTextToImage',
        description='This tool can generate an image from a depth '
        'image and a text. The text should be a series of English keywords '
        'separated by comma.',
        inputs=['image', 'text'],
        outputs=['image'],
    )

    @require('diffusers')
    def __init__(self,
                 toolmeta: Union[dict, ToolMeta] = DEFAULT_TOOLMETA,
                 parser: Callable = DefaultParser,
                 model: str = 'sd',
                 device: str = 'cuda'):
        super().__init__(toolmeta=toolmeta, parser=parser)
        assert model in ['sd', 'sdxl']
        self.model = model
        self.device = device

    def setup(self):
        if self.model == 'sdxl':
            self.pipe = load_sdxl(
                controlnet='diffusers/controlnet-depth-sdxl-1.0',
                controlnet_variant='fp16',
                device=self.device,
            )
        elif self.model == 'sd':
            self.pipe = load_sd(
                controlnet='lllyasviel/sd-controlnet-depth',
                device=self.device,
            )
        self.a_prompt = 'best quality, extremely detailed'
        self.n_prompt = 'longbody, lowres, bad anatomy, bad hands, '\
                        ' missing fingers, extra digit, fewer digits, '\
                        'cropped, worst quality, low quality'

    def apply(self, image: ImageIO, text: str) -> ImageIO:
        prompt = f'{text}, {self.a_prompt}'
        image = self.pipe(
            prompt,
            image=image.to_pil(),
            num_inference_steps=20,
            negative_prompt=self.n_prompt,
            controlnet_conditioning_scale=0.5,
        ).images[0]
        return ImageIO(image)
