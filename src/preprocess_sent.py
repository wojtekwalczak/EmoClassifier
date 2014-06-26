
class PreprocessSentence(object):

   def _stem_term(self, term_raw):
      aterm = aterm_raw.lower().strip()
      if len(aterm) < 3:
         return aterm
      if aterm in self.terms_by_root_form:
         return aterm
      if not aterm in self.allterms:
         return aterm
      for aroot in self.terms_by_root_form:
         if aterm in self.terms_by_root_form[aroot]:
            return aroot
      return aterm


   def _preprocess_sentence(self, sent):
      sent = re.sub(r"(.)\1{2,100}", r"\1", sent.replace('ł', 'l'))
      processed = sent[:]
      for aword_raw in re.findall(r"[^\W\d_ ]+", sent):
         stemmed = self._stem_word(aword_raw)
         if stemmed != aword_raw:
            processed = re.sub(aword_raw, stemmed, amessage)
      return processed

