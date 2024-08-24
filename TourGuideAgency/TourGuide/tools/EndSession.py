from agency_swarm.tools import BaseTool
class EndSession(BaseTool):
    """
    call this when the user is satisfied with your recommendations, and you can move on to the next session of recommendations.
    """
    def run(self):
        self._shared_state.set('finished', True)
