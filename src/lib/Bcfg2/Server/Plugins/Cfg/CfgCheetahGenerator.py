import copy
import logging
import Bcfg2.Server.Plugin
from Bcfg2.Server.Plugins.Cfg import CfgGenerator

logger = logging.getLogger(__name__)

try:
    import Cheetah.Template
    import Cheetah.Parser
    have_cheetah = True
except:
    have_cheetah = False


class CfgCheetahGenerator(CfgGenerator):
    __extensions__ = ['cheetah']
    settings = dict(useStackFrames=False)

    def __init__(self, fname, spec, encoding):
        CfgGenerator.__init__(self, fname, spec, encoding)
        if not have_cheetah:
            msg = "Cfg: Cheetah is not available: %s" % entry.get("name")
            logger.error(msg)
            raise Bcfg2.Server.Plugin.PluginExecutionError(msg)

    def get_data(self, entry, metadata):
        template = Cheetah.Template.Template(self.data,
                                             compilerSettings=self.settings)
        template.metadata = metadata
        template.path = entry.get('realname', entry.get('name'))
        template.source_path = self.path
        return template.respond()
