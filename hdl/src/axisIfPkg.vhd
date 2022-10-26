-- Author: michael
-- Version 1.0
-- Common record definitions for AXIS transactions.
-- requires VHDL-2008

library ieee;
use ieee.std_logic_1164.all;

package axisIfPkg is

  type axisIfDownstream_t is record
    tvalid  :       std_logic;
    tdata   :       std_logic_vector;
    tstrb   :       std_logic_vector;
    tkeep   :       std_logic_vector;
    tlast   :       std_logic_vector;
    tid     :       std_logic_vector;
    tdest   :       std_logic_vector;
    tuser   :       std_logic_vector;
  end record axisIfDownstream_t;

  type axisIfUpstream_t is record
    tready :       std_logic;
  end record axisIfUpstream_t;

  type axisIfDownstreamArray_t is array (<>) of axisIfDownstream_t;
  type axisIfUpstreamArray_t is array (<>) of axisIfUpstream_t;

end package axisIfPkg;
