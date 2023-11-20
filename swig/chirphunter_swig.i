/* -*- c++ -*- */

#define CHIRPHUNTER_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "chirphunter_swig_doc.i"

%{
#include "chirphunter/chirpgen.h"
#include "chirphunter/fhough.h"
%}

%include "chirphunter/chirpgen.h"
GR_SWIG_BLOCK_MAGIC2(chirphunter, chirpgen);
%include "chirphunter/fhough.h"
GR_SWIG_BLOCK_MAGIC2(chirphunter, fhough);
