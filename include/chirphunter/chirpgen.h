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

#ifndef INCLUDED_CHIRPHUNTER_CHIRPGEN_H
#define INCLUDED_CHIRPHUNTER_CHIRPGEN_H

#include <chirphunter/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace chirphunter {

    /*!
     * \brief <+description of block+>
     * \ingroup chirphunter
     *
     */
    class CHIRPHUNTER_API chirpgen : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<chirpgen> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of chirphunter::chirpgen.
       *
       * To avoid accidental use of raw pointers, chirphunter::chirpgen's
       * constructor is in a private implementation
       * class. chirphunter::chirpgen::make is the public interface for
       * creating new instances.
       */
      static sptr make(float f0, float chirp_rate, float samp_rate);
    };

  } // namespace chirphunter
} // namespace gr

#endif /* INCLUDED_CHIRPHUNTER_CHIRPGEN_H */

