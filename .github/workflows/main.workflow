workflow "New workflow" {
  on = "push"
  resolves = ["Hello World"]
}

action "Hello World" {
  uses = "./say_hello.sh"
  env = {
    MY_NAME = "KeisukeYamashita"
  }
  args = "\"Hello world, I'm $MY_NAME!\""
}
