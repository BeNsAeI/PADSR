import click
import cmd

class REPL(cmd.Cmd):
    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx

    def default(self, line):
        subcommand = cli.commands.get(line)
        if subcommand:
            self.ctx.invoke(subcommand)
        else:
            return cmd.Cmd.default(self, line)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        repl = REPL(ctx)
        repl.cmdloop()

@cli.command()
def a():
    """The `a` command prints an 'a'."""
    print "a"

@cli.command()
def b():
    """The `b` command prints a 'b'."""
    print "b"

if __name__ == "__main__":
    print "The `a` command prints an 'a'."
    print "The `b` command prints a 'b'."
    print "Ctrl-C to exit"
    cli()
