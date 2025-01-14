# This file is part of arduino-cli.
#
# Copyright 2020 ARDUINO SA (http://www.arduino.cc/)
#
# This software is released under the GNU General Public License version 3,
# which covers the main part of arduino-cli.
# The terms of this license can be found at:
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# You can be released from the requirements of the above licenses by purchasing
# a commercial license. Buying such a license is mandatory if you want to modify or
# otherwise use the software for commercial activities involving the Arduino
# software without disclosing the source code of your own applications. To purchase
# a commercial license, send an email to license@arduino.cc.


def test_compile_with_profiles(run_command, copy_sketch):
    # Init the environment explicitly
    run_command(["core", "update-index"])

    sketch_path = copy_sketch("sketch_with_profile")

    # use profile without a required library -> should fail
    assert run_command(["lib", "install", "Arduino_JSON"])
    result = run_command(["compile", "-m", "avr1", sketch_path])
    assert result.failed

    # use profile with the required library -> should succeed
    result = run_command(["compile", "-m", "avr2", sketch_path])
    assert result.ok


def test_builder_did_not_catch_libs_from_unused_platforms(run_command, copy_sketch):
    # Init the environment explicitly
    run_command(["core", "update-index"])

    sketch_path = copy_sketch("sketch_with_error_including_wire")

    # install two platforms with the Wire library bundled
    assert run_command(["core", "install", "arduino:avr"])
    assert run_command(["core", "install", "arduino:samd"])

    # compile for AVR
    result = run_command(["compile", "-b", "arduino:avr:uno", sketch_path])
    assert result.failed

    # check that the libary resolver did not take the SAMD bundled Wire library into account
    assert "samd" not in result.stdout
    assert "samd" not in result.stderr
