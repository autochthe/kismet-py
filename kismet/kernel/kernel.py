from ipykernel.kernelbase import Kernel
from kismet.parser import KismetParser


class KismetKernel(Kernel):
    """
    IPython Kernel for the Kismet Parser
    """
    implementation = "Kismet"
    implementation_version = "0.1"
    language = "Kismet"
    language_version = "0.1"
    banner = "Kismet kernel - dice parser"

    parser = KismetParser()

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        output = str(self.parser.parse(code))
        if not silent:
            stream_content = {"name": "stdout", "text": output}
            self.send_response(self.iopub_socket, "stream", stream_content)

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }
