from options.ToolOptions import ToolOptions
from options.JobOptions import JobOptions
from options.OutputOptions import OutputOptions

class Options:

    def __init__(self, tool: ToolOptions, job: JobOptions, output: OutputOptions):
        if tool is None:
            raise ValueError('Tool options must be populated')
        elif job is None:
            raise ValueError('Job options must be populated')
        elif output is None:
            raise ValueError('Output options must be populated')

        self._tool = tool
        self._job = job
        self._output = output

    tool = property(fget=lambda self: self._tool)
    job = property(fget=lambda self: self._job)
    output = property(fget=lambda self: self._output)
