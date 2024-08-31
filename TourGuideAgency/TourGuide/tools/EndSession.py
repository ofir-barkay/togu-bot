from agency_swarm.tools import BaseTool
class EndSession(BaseTool):
    """
    call this when the user is satisfied with your recommendations, to let them know the session has ended.
    """
    def run(self):
        self._shared_state.set('finished', True)
