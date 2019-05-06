/* -*- c++ -*- */
/*
 * Copyright 2019 Ryan Tse.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <iostream>
#include <gnuradio/io_signature.h>
#include "chirpgen_impl.h"

namespace gr {
  namespace chirphunter {

    /** Public constructor (see chirpgen_impl) */
    chirpgen::sptr chirpgen::make(float f0, float chirp_rate, float samp_rate) {
      return gnuradio::get_initial_sptr
        (new chirpgen_impl(f0, chirp_rate, samp_rate));
    }


    /**
     * Construct chiprgen block
     * Populate the lookup table
     */
    chirpgen_impl::chirpgen_impl(float _f0, float _chirp_rate, float _samp_rate)
      : gr::sync_block("chirpgen",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(gr_complex))) {

          f0 = _f0;
          chirp_rate = _chirp_rate;
          fs = _samp_rate;


          // Populate chirp_lut 
          for (int i = 0; i < LUT_SIZE; i++) {
              chirp_lut[i].real((float) cos(-2.0 * M_PI * ((double) i) / ((double) LUT_SIZE)));
              chirp_lut[i].imag((float) sin(-2.0 * M_PI * ((double) i) / ((double) LUT_SIZE)));
          }
      }

    /*
     * Our virtual destructor.
     */
    chirpgen_impl::~chirpgen_impl() {
    }

    /**
     * Set the output to be the value of the chirp lookup table
     */
    int chirpgen_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items) {

      gr_complex *out = (gr_complex *) output_items[0];

      /*
      double chirpt = curr_t / fs;
      double time  = (f0 + 0.5 * chirp_rate * chirpt) * chirpt;
      int64_t idx = (int64_t) didxr % LUT_SIZE;
      */

      double time = 0;
      double theta = 0;

      /* Compute e^{2\pi i \omega} where omega varies with t
       * as \omega = (f_0 + m * t) * t */
      for (int i = 0; i < noutput_items; i++) {
          time = curr_t / fs;
          theta = (f0 + 0.5 * chirp_rate * time) * time;

          out[i].real(cos(2.0 * M_PI * theta));
          out[i].imag(sin(2.0 * M_PI * theta));

          curr_t++;
      }

      return noutput_items;
    }

  } /* namespace chirphunter */
} /* namespace gr */

