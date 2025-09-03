/* -*- c++ -*- */
/*
 * Copyright 2025 gr-wavetrap author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */


 #ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "head_w_rst_impl.h"


namespace gr {
  namespace wavetrap {

    head_w_rst::sptr
    head_w_rst::make(size_t sizeof_stream_item, uint64_t nitems)
    {
      return gnuradio::get_initial_sptr
        (new head_w_rst_impl(sizeof_stream_item, nitems));
    }

    head_w_rst_impl::head_w_rst_impl(size_t sizeof_stream_item, uint64_t nitems)
      : gr::block("head_w_rst",
              gr::io_signature::make(1, 1, sizeof_stream_item),
              gr::io_signature::make(1, 1, sizeof_stream_item)),
              d_nitems(nitems),
              d_ncopied_items(0),
              d_dump_buff(false)
    {
      status_num = 0;
      status_port = pmt::string_to_symbol("status");
      message_port_register_out(status_port);

      message_port_register_in(pmt::mp("reset"));
      //set_msg_handler(pmt::mp("reset"),
        //[this](pmt::pmt_t& msg) {reset(msg); });
      set_msg_handler(pmt::mp("reset"),
        [this](const pmt::pmt_t& msg) { this->reset(msg); });
    }

    head_w_rst_impl::~head_w_rst_impl()
    {
    }

    void head_w_rst_impl::set_length(uint64_t nitems) {
      gr::thread::scoped_lock guard(d_setlock);
      d_nitems = nitems;
      d_ncopied_items = nitems;

    }
    
    void head_w_rst_impl::reset(const pmt::pmt_t& msg) {
      if (pmt::is_pair(msg)) { 
        pmt::pmt_t msg_val = pmt::cdr(msg); // extract value from message pair
        if (pmt::is_bool(msg_val)) {
          bool dump_buff = pmt::to_bool(msg_val);
          if(dump_buff) {
            if(status_num != 1){
                  message_port_pub(status_port, pmt::string_to_symbol("RESET") );
                  status_num = 1;
            }
            d_ncopied_items = 0; 
            d_dump_buff = dump_buff;
          }
          } else {
              GR_LOG_WARN(d_logger,
                          "handle_enable: Non-PMT type received, expecting Boolean PMT");
          }
      }
        else {
          GR_LOG_WARN(d_logger,
                          "handle_enable: No PMT Pair received, expecting PMT Pair");
        }
    }
    //status message numbers (to avoid repetitive sending)
    //default       0
    //RESET         1
    //IN PROGRESS   2
    //FINISHED      3

    int
    head_w_rst_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items_,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      int ninput_items = std::min(ninput_items_[0], noutput_items);

      if(d_dump_buff) {
        //purge buffer after reset - dump remaining input samples 
        d_dump_buff = false;
        consume_each(ninput_items);
        return 0;
      }

      if (d_ncopied_items >= d_nitems){
        //already copied n items, skip rest
        if(status_num != 3){
          message_port_pub(status_port, pmt::string_to_symbol("FINISHED"));
          status_num = 3;
        }
        consume_each(ninput_items);
        return 0;
      }

      unsigned n = std::min(d_nitems - d_ncopied_items, (uint64_t)noutput_items);

      if (n == 0){
        //cant consume if there are 0 items
        //consume_each(0);
        return 0;
      }
      
      //copy items to out
      if(status_num != 2) {
        message_port_pub(status_port, pmt::string_to_symbol("IN PROGRESS"));
        status_num = 2;
      }

      memcpy(output_items[0], input_items[0], n * input_signature()->sizeof_stream_item(0));
      d_ncopied_items += n;
      consume_each(n);
      return n;
    }

  } /* namespace wavetrap */
} /* namespace gr */

