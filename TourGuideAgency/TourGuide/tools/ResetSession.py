from agency_swarm.tools import BaseTool
class ResetSession(BaseTool):
    """
    call this when prompted to, so you can move on to the next session of recommendations after the previous one was finished
    """
    def run(self):
        self._shared_state.set('finished', False)
