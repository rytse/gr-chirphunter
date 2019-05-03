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

#ifndef INCLUDED_CHIRPHUNTER_CHIRPGEN_IMPL_H
#define INCLUDED_CHIRPHUNTER_CHIRPGEN_IMPL_H

#include <chirphunter/chirpgen.h>

namespace gr {
  namespace chirphunter {

    class chirpgen_impl : public chirpgen
    {
     private:
        /** Number of elements in the chirp lookup table */
        static const int LUT_SIZE = 8192 * 8192;

        /** Look up table that has the values of the chirp
         * template $e^{2\pi j (f_0 + mt)t}$ precomputed. This
         * is populated during construction so that the block
         * need not recompute the known chirp at runtime */
        gr_complex chirp_lut[LUT_SIZE];

        /** Current time (seconds) */
        double curr_t = 0;

        /** Sampling rate (samples / second) */
        float f0;
        float chirp_rate;
        float fs;

     public:
      chirpgen_impl(float f0, float chirp_rate, float samp_rate);
      ~chirpgen_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace chirphunter
} // namespace gr

#endif /* INCLUDED_CHIRPHUNTER_CHIRPGEN_IMPL_H */

