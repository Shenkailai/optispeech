import os
# if os.environ.get("version","v1")=="v1":
#   from text.symbols import symbols
# else:
#   from text.symbols2 import symbols
import LangSegment
from optispeech.text2.cleaner import clean_text
LangSegment.setfilters(["zh","en"])

from optispeech.text.tokenizers import BaseTokenizer

from optispeech.text2 import symbols as symbols_v1
from optispeech.text2 import symbols2 as symbols_v2

_symbol_to_id_v1 = {s: i for i, s in enumerate(symbols_v1.symbols)}
_symbol_to_id_v2 = {s: i for i, s in enumerate(symbols_v2.symbols)}

def cleaned_text_to_sequence(cleaned_text, version=None):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  if version is None:version=os.environ.get('version', 'v2')
  if version == "v1":
    phones = [_symbol_to_id_v1[symbol] for symbol in cleaned_text]
  else:
    phones = [_symbol_to_id_v2[symbol] for symbol in cleaned_text]

  return phones


def intersperse(lst, item):
  result = [item] * (len(lst) * 2 + 1)
  result[1::2] = lst
  return result

class MixTokenizer(BaseTokenizer):
  name = "mix"
  input_symbols = dict(_symbol_to_id_v2)
  special_symbols = dict(
      pad=None,
      bos=None,
      eos=None,
  )

  def __call__( self, text: str, language: str, *, split_sentences: bool = True
    ) -> tuple[list[int] | list[list[int]], str]:
      text_segments = []
      for segment in LangSegment.getTexts(text):
          cleaned_text, _, normtext = clean_text(segment["text"], segment["lang"])
          text_segments.append(cleaned_text)
      phones = sum(text_segments, [])
      text_id = cleaned_text_to_sequence(phones)
      # add blank token between segments
      text_id = intersperse(text_id, 95)
      return text_id, phones
