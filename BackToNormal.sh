ip netns delete blue
ip netns delete red
ifconfig br-test down
brctl delbr br-test
