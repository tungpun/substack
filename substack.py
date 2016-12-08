import argparse
import sys

from substack.data.profile import Profile
from substack.substack_core import SubStack


def main():
    profile = Profile("empty")
    profile.set_target("bkav.com")

    sub_stack = SubStack()
    sub_stack.set_profile(profile)

    sub_stack.start()

    # print len(result)


if __name__ == "__main__":
    main()
