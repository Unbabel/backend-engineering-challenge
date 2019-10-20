package com.unbabel

case class Event(
                  timestamp: String,
                  translation_id: String,
                  lang_src: String,
                  lang_trg: String,
                  client: String,
                  name: String,
                  duration: Long,
                  nr_words: Long
                )
