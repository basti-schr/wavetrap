/* -*- c++ -*- */
/*
 * Copyright 2025 gr-wavetrap author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_WAVETRAP_HEAD_W_RST_IMPL_H
#define INCLUDED_WAVETRAP_HEAD_W_RST_IMPL_H

#include <gnuradio/wavetrap/head_w_rst.h>

namespace gr {
  namespace wavetrap {

    class head_w_rst_impl : public head_w_rst
    {
     private:
      uint64_t d_nitems;
      uint64_t d_ncopied_items;
      bool d_dump_buff;
      pmt::pmt_t status_port;
      int8_t status_num;
     public:
      head_w_rst_impl(size_t sizeof_stream_item, uint64_t nitems);
      ~head_w_rst_impl();
      
      void reset(const pmt::pmt_t& msg);
      void set_length(uint64_t nitems);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace wavetrap
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_HEAD_W_RST_IMPL_H */

