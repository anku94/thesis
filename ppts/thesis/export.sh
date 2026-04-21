#!/bin/bash
# Export slides with transforms

INPUT="thesis_slides.pdf"
OUTPUT="thesis_slides_exported.pdf"
SLIDES_START=1
SLIDES_END=46

TEMP_FILE="temp_export.pdf"

# Extract slides
pdftk "$INPUT" cat ${SLIDES_START}-${SLIDES_END} output "$TEMP_FILE"

# Remove orphaned resources and compress images
# Note: embedded movies are dropped by gs (not supported in pdfwrite)
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.5 \
   -dNOPAUSE -dBATCH -dQUIET \
   -dPrinted=false \
   -dDownsampleColorImages=true \
   -dColorImageResolution=150 \
   -dDownsampleGrayImages=true \
   -dGrayImageResolution=150 \
   -dDownsampleMonoImages=true \
   -dMonoImageResolution=150 \
   -dCompressFonts=true \
   -dSubsetFonts=true \
   -sOutputFile="$OUTPUT" \
   "$TEMP_FILE"

rm -f "$TEMP_FILE"

echo "Exported slides ${SLIDES_START}-${SLIDES_END} to ${OUTPUT}"
