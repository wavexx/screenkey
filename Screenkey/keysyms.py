# https://www.cl.cam.ac.uk/~mgk25/ucs/keysyms.txt
# Mapping of X11 keysyms to ISO 10646 / Unicode
#
# The "X11 Window System Protocol" standard (Release 6.4) defines in
# Appendix A the keysym codes. These 29-bit integer values identify
# characters or functions associated with each key (e.g., via the
# visible engraving) of a keyboard layout. In addition, mnemonic macro
# names are provided for the keysyms in the C header file
# <X11/keysymdef.h>. These are compiled (by xc/lib/X11/util/
# makekeys.c) into a hash table that can be accessed with X11 library
# functions such as XStringToKeysym() and XKeysymToString().
#
# The creation of the keysym codes predates ISO 10646 / Unicode, but
# they represent a similar attempt to merge several existing coded
# character sets (mostly early drafts of ISO 8859, as well as some --
# long since forgotten -- DEC font encodings). X.Org and XFree86 have
# agreed that for any future extension of the keysyms with characters
# already found in ISO 10646 / Unicode, the following algorithm will
# be used. The new keysym code position will simply be the character's
# Unicode number plus 0x01000000. The keysym codes in the range
# 0x01000100 0x0110ffff are now reserved to represent Unicode
# characters in the range U0100 to U10FFFF. (Note that the ISO 8859-1
# characters that make up Unicode positions below U0100 are excluded
# from this rule, as they are already covered by the keysyms of the
# same value.)
#
# While most newer Unicode-based X11 clients do already accept
# Unicode-mapped keysyms in the range 0x01000100 to 0x0110ffff, it
# will remain necessary for clients -- in the interest of
# compatibility with existing servers -- to also understand the
# existing keysym values. Clients can use the table below to map the
# pre-Unicode keysym values (0x0100 to 0x20ff) to the corresponding
# Unicode characters for further processing.
#
# The following fields are used in this mapping table:
#
# 1    The hexadecimal X11 keysym number (as defined in Appendix A of
#      the X11 protocol specification and as listed in <X11/keysymdef.h>)
#
# 2    The corresponding Unicode position
#      (U0000 means that there is no equivalent Unicode character)
#
# 3    Status of this keysym and its Unicode mapping
#
#         .  regular -- This is a regular well-established keysym with
#            a straightforward Unicode equivalent (e.g., any keysym
#            derived from ISO 8859). There can be at most one regular
#            keysym associated with each Unicode character.
#
#         d  duplicate -- This keysym has the same Unicode mapping as
#            another one with status 'regular'. It represents a case
#            where keysyms distinguish between several characters that
#            Unicode has unified into a single one (examples are
#            several APL symbols)
#
#         o  obsolete -- While it may be possible to find a Unicode of
#            similar name, the exact semantics of this keysym are
#            unclear, because the font or character set from which it
#            came has never been widely used. Examples are various
#            symbols from the DEC Publishing character set, which may
#            have been used in a special font shipped with the
#            DECwrite product. Where no similar Unicode character
#            can be identified, U0000 is used in column 2.
#
#         f  function -- While it may be possible to find a Unicode
#            of similar name, this keysym differs semantically
#            substantially from the corresponding Unicode character,
#            because it describes a particular function key or will
#            first have to be processed by an input method that will
#            translate it into a proper stream of Unicode characters.
#
#         r  remove -- This is a bogus keysym that was added in error,
#            is not used in any known keyboard layout, and should be
#            removed from both <X11/keysymdef.h> and the standard.
#
#         u  unicode-remap -- This keysym was added rather recently to
#            the <X11/keysymdef.h> of XFree86, but into a number range
#            reserved for future extensions of the standard by
#            X.Org. It is not widely used at present, but its name
#            appears to be sufficiently useful and it should therefore
#            be directly mapped to Unicode in the 0x1xxxxxx range in
#            future versions of <X11/keysymdef.h>. This way, the macro
#            name will be preserved, but the standard will not have to
#            be extended.
#
#      Recommendations for using the keysym status:
#
#        - All keysyms with status regular, duplicate, obsolete and
#          function should be listed in Appendix A of the X11 protocol
#          spec.
#
#        - All keysyms except for those with status remove should be
#          listed in <X11/keysymdef.h>.
#
#        - Keysyms with status duplicate, obsolete, and remove should
#          not be used in future keyboard layouts, as there are other
#          keysyms with status regular, function and unicode-remap
#          that give access to the same Unicode characters.
#
#        - Keysym to Unicode conversion tables in clients should include
#          all mappings except those with status function and those
#          with U0000.
#
# #    comment marker
#
# 4    the name of the X11 keysym macro without the leading XK_,
#      as defined in <X11/keysymdef.h>
#
# The last columns may be followed by comments copied from <X11/keysymdef.h>.
# A keysym may be listed several times, if there are several macro names
# associated with it in <X11/keysymdef.h>.
#
# Author: Markus Kuhn <http://www.cl.cam.ac.uk/~mgk25/>
# Date:   2004-08-08
#
# This table evolved out of an earlier one by Richard Verhoeven, TU Eindhoven.

KEYSYMS = {

# We begin with the original keysyms found in X11R6.4
0x0020:   [u'\u0020',   '.'],   # space
0x0021:   [u'\u0021',   '.'],   # exclam
0x0022:   [u'\u0022',   '.'],   # quotedbl
0x0023:   [u'\u0023',   '.'],   # numbersign
0x0024:   [u'\u0024',   '.'],   # dollar
0x0025:   [u'\u0025',   '.'],   # percent
0x0026:   [u'\u0026',   '.'],   # ampersand
0x0027:   [u'\u0027',   '.'],   # apostrophe
0x0027:   [u'\u0027',   '.'],   # quoteright	/* deprecated */
0x0028:   [u'\u0028',   '.'],   # parenleft
0x0029:   [u'\u0029',   '.'],   # parenright
0x002a:   [u'\u002a',   '.'],   # asterisk
0x002b:   [u'\u002b',   '.'],   # plus
0x002c:   [u'\u002c',   '.'],   # comma
0x002d:   [u'\u002d',   '.'],   # minus
0x002e:   [u'\u002e',   '.'],   # period
0x002f:   [u'\u002f',   '.'],   # slash
0x0030:   [u'\u0030',   '.'],   # 0
0x0031:   [u'\u0031',   '.'],   # 1
0x0032:   [u'\u0032',   '.'],   # 2
0x0033:   [u'\u0033',   '.'],   # 3
0x0034:   [u'\u0034',   '.'],   # 4
0x0035:   [u'\u0035',   '.'],   # 5
0x0036:   [u'\u0036',   '.'],   # 6
0x0037:   [u'\u0037',   '.'],   # 7
0x0038:   [u'\u0038',   '.'],   # 8
0x0039:   [u'\u0039',   '.'],   # 9
0x003a:   [u'\u003a',   '.'],   # colon
0x003b:   [u'\u003b',   '.'],   # semicolon
0x003c:   [u'\u003c',   '.'],   # less
0x003d:   [u'\u003d',   '.'],   # equal
0x003e:   [u'\u003e',   '.'],   # greater
0x003f:   [u'\u003f',   '.'],   # question
0x0040:   [u'\u0040',   '.'],   # at
0x0041:   [u'\u0041',   '.'],   # A
0x0042:   [u'\u0042',   '.'],   # B
0x0043:   [u'\u0043',   '.'],   # C
0x0044:   [u'\u0044',   '.'],   # D
0x0045:   [u'\u0045',   '.'],   # E
0x0046:   [u'\u0046',   '.'],   # F
0x0047:   [u'\u0047',   '.'],   # G
0x0048:   [u'\u0048',   '.'],   # H
0x0049:   [u'\u0049',   '.'],   # I
0x004a:   [u'\u004a',   '.'],   # J
0x004b:   [u'\u004b',   '.'],   # K
0x004c:   [u'\u004c',   '.'],   # L
0x004d:   [u'\u004d',   '.'],   # M
0x004e:   [u'\u004e',   '.'],   # N
0x004f:   [u'\u004f',   '.'],   # O
0x0050:   [u'\u0050',   '.'],   # P
0x0051:   [u'\u0051',   '.'],   # Q
0x0052:   [u'\u0052',   '.'],   # R
0x0053:   [u'\u0053',   '.'],   # S
0x0054:   [u'\u0054',   '.'],   # T
0x0055:   [u'\u0055',   '.'],   # U
0x0056:   [u'\u0056',   '.'],   # V
0x0057:   [u'\u0057',   '.'],   # W
0x0058:   [u'\u0058',   '.'],   # X
0x0059:   [u'\u0059',   '.'],   # Y
0x005a:   [u'\u005a',   '.'],   # Z
0x005b:   [u'\u005b',   '.'],   # bracketleft
0x005c:   [u'\u005c',   '.'],   # backslash
0x005d:   [u'\u005d',   '.'],   # bracketright
0x005e:   [u'\u005e',   '.'],   # asciicircum
0x005f:   [u'\u005f',   '.'],   # underscore
0x0060:   [u'\u0060',   '.'],   # grave
0x0060:   [u'\u0060',   '.'],   # quoteleft	/* deprecated */
0x0061:   [u'\u0061',   '.'],   # a
0x0062:   [u'\u0062',   '.'],   # b
0x0063:   [u'\u0063',   '.'],   # c
0x0064:   [u'\u0064',   '.'],   # d
0x0065:   [u'\u0065',   '.'],   # e
0x0066:   [u'\u0066',   '.'],   # f
0x0067:   [u'\u0067',   '.'],   # g
0x0068:   [u'\u0068',   '.'],   # h
0x0069:   [u'\u0069',   '.'],   # i
0x006a:   [u'\u006a',   '.'],   # j
0x006b:   [u'\u006b',   '.'],   # k
0x006c:   [u'\u006c',   '.'],   # l
0x006d:   [u'\u006d',   '.'],   # m
0x006e:   [u'\u006e',   '.'],   # n
0x006f:   [u'\u006f',   '.'],   # o
0x0070:   [u'\u0070',   '.'],   # p
0x0071:   [u'\u0071',   '.'],   # q
0x0072:   [u'\u0072',   '.'],   # r
0x0073:   [u'\u0073',   '.'],   # s
0x0074:   [u'\u0074',   '.'],   # t
0x0075:   [u'\u0075',   '.'],   # u
0x0076:   [u'\u0076',   '.'],   # v
0x0077:   [u'\u0077',   '.'],   # w
0x0078:   [u'\u0078',   '.'],   # x
0x0079:   [u'\u0079',   '.'],   # y
0x007a:   [u'\u007a',   '.'],   # z
0x007b:   [u'\u007b',   '.'],   # braceleft
0x007c:   [u'\u007c',   '.'],   # bar
0x007d:   [u'\u007d',   '.'],   # braceright
0x007e:   [u'\u007e',   '.'],   # asciitilde
0x00a0:   [u'\u00a0',   '.'],   # nobreakspace
0x00a1:   [u'\u00a1',   '.'],   # exclamdown
0x00a2:   [u'\u00a2',   '.'],   # cent
0x00a3:   [u'\u00a3',   '.'],   # sterling
0x00a4:   [u'\u00a4',   '.'],   # currency
0x00a5:   [u'\u00a5',   '.'],   # yen
0x00a6:   [u'\u00a6',   '.'],   # brokenbar
0x00a7:   [u'\u00a7',   '.'],   # section
0x00a8:   [u'\u00a8',   '.'],   # diaeresis
0x00a9:   [u'\u00a9',   '.'],   # copyright
0x00aa:   [u'\u00aa',   '.'],   # ordfeminine
0x00ab:   [u'\u00ab',   '.'],   # guillemotleft	/* left angle quotation mark */
0x00ac:   [u'\u00ac',   '.'],   # notsign
0x00ad:   [u'\u00ad',   '.'],   # hyphen
0x00ae:   [u'\u00ae',   '.'],   # registered
0x00af:   [u'\u00af',   '.'],   # macron
0x00b0:   [u'\u00b0',   '.'],   # degree
0x00b1:   [u'\u00b1',   '.'],   # plusminus
0x00b2:   [u'\u00b2',   '.'],   # twosuperior
0x00b3:   [u'\u00b3',   '.'],   # threesuperior
0x00b4:   [u'\u00b4',   '.'],   # acute
0x00b5:   [u'\u00b5',   '.'],   # mu
0x00b6:   [u'\u00b6',   '.'],   # paragraph
0x00b7:   [u'\u00b7',   '.'],   # periodcentered
0x00b8:   [u'\u00b8',   '.'],   # cedilla
0x00b9:   [u'\u00b9',   '.'],   # onesuperior
0x00ba:   [u'\u00ba',   '.'],   # masculine
0x00bb:   [u'\u00bb',   '.'],   # guillemotright	/* right angle quotation mark */
0x00bc:   [u'\u00bc',   '.'],   # onequarter
0x00bd:   [u'\u00bd',   '.'],   # onehalf
0x00be:   [u'\u00be',   '.'],   # threequarters
0x00bf:   [u'\u00bf',   '.'],   # questiondown
0x00c0:   [u'\u00c0',   '.'],   # Agrave
0x00c1:   [u'\u00c1',   '.'],   # Aacute
0x00c2:   [u'\u00c2',   '.'],   # Acircumflex
0x00c3:   [u'\u00c3',   '.'],   # Atilde
0x00c4:   [u'\u00c4',   '.'],   # Adiaeresis
0x00c5:   [u'\u00c5',   '.'],   # Aring
0x00c6:   [u'\u00c6',   '.'],   # AE
0x00c7:   [u'\u00c7',   '.'],   # Ccedilla
0x00c8:   [u'\u00c8',   '.'],   # Egrave
0x00c9:   [u'\u00c9',   '.'],   # Eacute
0x00ca:   [u'\u00ca',   '.'],   # Ecircumflex
0x00cb:   [u'\u00cb',   '.'],   # Ediaeresis
0x00cc:   [u'\u00cc',   '.'],   # Igrave
0x00cd:   [u'\u00cd',   '.'],   # Iacute
0x00ce:   [u'\u00ce',   '.'],   # Icircumflex
0x00cf:   [u'\u00cf',   '.'],   # Idiaeresis
0x00d0:   [u'\u00d0',   '.'],   # ETH
0x00d0:   [u'\u00d0',   '.'],   # Eth	/* deprecated */
0x00d1:   [u'\u00d1',   '.'],   # Ntilde
0x00d2:   [u'\u00d2',   '.'],   # Ograve
0x00d3:   [u'\u00d3',   '.'],   # Oacute
0x00d4:   [u'\u00d4',   '.'],   # Ocircumflex
0x00d5:   [u'\u00d5',   '.'],   # Otilde
0x00d6:   [u'\u00d6',   '.'],   # Odiaeresis
0x00d7:   [u'\u00d7',   '.'],   # multiply
0x00d8:   [u'\u00d8',   '.'],   # Ooblique
0x00d9:   [u'\u00d9',   '.'],   # Ugrave
0x00da:   [u'\u00da',   '.'],   # Uacute
0x00db:   [u'\u00db',   '.'],   # Ucircumflex
0x00dc:   [u'\u00dc',   '.'],   # Udiaeresis
0x00dd:   [u'\u00dd',   '.'],   # Yacute
0x00de:   [u'\u00de',   '.'],   # THORN
0x00de:   [u'\u00de',   '.'],   # Thorn	/* deprecated */
0x00df:   [u'\u00df',   '.'],   # ssharp
0x00e0:   [u'\u00e0',   '.'],   # agrave
0x00e1:   [u'\u00e1',   '.'],   # aacute
0x00e2:   [u'\u00e2',   '.'],   # acircumflex
0x00e3:   [u'\u00e3',   '.'],   # atilde
0x00e4:   [u'\u00e4',   '.'],   # adiaeresis
0x00e5:   [u'\u00e5',   '.'],   # aring
0x00e6:   [u'\u00e6',   '.'],   # ae
0x00e7:   [u'\u00e7',   '.'],   # ccedilla
0x00e8:   [u'\u00e8',   '.'],   # egrave
0x00e9:   [u'\u00e9',   '.'],   # eacute
0x00ea:   [u'\u00ea',   '.'],   # ecircumflex
0x00eb:   [u'\u00eb',   '.'],   # ediaeresis
0x00ec:   [u'\u00ec',   '.'],   # igrave
0x00ed:   [u'\u00ed',   '.'],   # iacute
0x00ee:   [u'\u00ee',   '.'],   # icircumflex
0x00ef:   [u'\u00ef',   '.'],   # idiaeresis
0x00f0:   [u'\u00f0',   '.'],   # eth
0x00f1:   [u'\u00f1',   '.'],   # ntilde
0x00f2:   [u'\u00f2',   '.'],   # ograve
0x00f3:   [u'\u00f3',   '.'],   # oacute
0x00f4:   [u'\u00f4',   '.'],   # ocircumflex
0x00f5:   [u'\u00f5',   '.'],   # otilde
0x00f6:   [u'\u00f6',   '.'],   # odiaeresis
0x00f7:   [u'\u00f7',   '.'],   # division
0x00f8:   [u'\u00f8',   '.'],   # oslash
0x00f9:   [u'\u00f9',   '.'],   # ugrave
0x00fa:   [u'\u00fa',   '.'],   # uacute
0x00fb:   [u'\u00fb',   '.'],   # ucircumflex
0x00fc:   [u'\u00fc',   '.'],   # udiaeresis
0x00fd:   [u'\u00fd',   '.'],   # yacute
0x00fe:   [u'\u00fe',   '.'],   # thorn
0x00ff:   [u'\u00ff',   '.'],   # ydiaeresis
0x01a1:   [u'\u0104',   '.'],   # Aogonek
0x01a2:   [u'\u02d8',   '.'],   # breve
0x01a3:   [u'\u0141',   '.'],   # Lstroke
0x01a5:   [u'\u013d',   '.'],   # Lcaron
0x01a6:   [u'\u015a',   '.'],   # Sacute
0x01a9:   [u'\u0160',   '.'],   # Scaron
0x01aa:   [u'\u015e',   '.'],   # Scedilla
0x01ab:   [u'\u0164',   '.'],   # Tcaron
0x01ac:   [u'\u0179',   '.'],   # Zacute
0x01ae:   [u'\u017d',   '.'],   # Zcaron
0x01af:   [u'\u017b',   '.'],   # Zabovedot
0x01b1:   [u'\u0105',   '.'],   # aogonek
0x01b2:   [u'\u02db',   '.'],   # ogonek
0x01b3:   [u'\u0142',   '.'],   # lstroke
0x01b5:   [u'\u013e',   '.'],   # lcaron
0x01b6:   [u'\u015b',   '.'],   # sacute
0x01b7:   [u'\u02c7',   '.'],   # caron
0x01b9:   [u'\u0161',   '.'],   # scaron
0x01ba:   [u'\u015f',   '.'],   # scedilla
0x01bb:   [u'\u0165',   '.'],   # tcaron
0x01bc:   [u'\u017a',   '.'],   # zacute
0x01bd:   [u'\u02dd',   '.'],   # doubleacute
0x01be:   [u'\u017e',   '.'],   # zcaron
0x01bf:   [u'\u017c',   '.'],   # zabovedot
0x01c0:   [u'\u0154',   '.'],   # Racute
0x01c3:   [u'\u0102',   '.'],   # Abreve
0x01c5:   [u'\u0139',   '.'],   # Lacute
0x01c6:   [u'\u0106',   '.'],   # Cacute
0x01c8:   [u'\u010c',   '.'],   # Ccaron
0x01ca:   [u'\u0118',   '.'],   # Eogonek
0x01cc:   [u'\u011a',   '.'],   # Ecaron
0x01cf:   [u'\u010e',   '.'],   # Dcaron
0x01d0:   [u'\u0110',   '.'],   # Dstroke
0x01d1:   [u'\u0143',   '.'],   # Nacute
0x01d2:   [u'\u0147',   '.'],   # Ncaron
0x01d5:   [u'\u0150',   '.'],   # Odoubleacute
0x01d8:   [u'\u0158',   '.'],   # Rcaron
0x01d9:   [u'\u016e',   '.'],   # Uring
0x01db:   [u'\u0170',   '.'],   # Udoubleacute
0x01de:   [u'\u0162',   '.'],   # Tcedilla
0x01e0:   [u'\u0155',   '.'],   # racute
0x01e3:   [u'\u0103',   '.'],   # abreve
0x01e5:   [u'\u013a',   '.'],   # lacute
0x01e6:   [u'\u0107',   '.'],   # cacute
0x01e8:   [u'\u010d',   '.'],   # ccaron
0x01ea:   [u'\u0119',   '.'],   # eogonek
0x01ec:   [u'\u011b',   '.'],   # ecaron
0x01ef:   [u'\u010f',   '.'],   # dcaron
0x01f0:   [u'\u0111',   '.'],   # dstroke
0x01f1:   [u'\u0144',   '.'],   # nacute
0x01f2:   [u'\u0148',   '.'],   # ncaron
0x01f5:   [u'\u0151',   '.'],   # odoubleacute
0x01f8:   [u'\u0159',   '.'],   # rcaron
0x01f9:   [u'\u016f',   '.'],   # uring
0x01fb:   [u'\u0171',   '.'],   # udoubleacute
0x01fe:   [u'\u0163',   '.'],   # tcedilla
0x01ff:   [u'\u02d9',   '.'],   # abovedot
0x02a1:   [u'\u0126',   '.'],   # Hstroke
0x02a6:   [u'\u0124',   '.'],   # Hcircumflex
0x02a9:   [u'\u0130',   '.'],   # Iabovedot
0x02ab:   [u'\u011e',   '.'],   # Gbreve
0x02ac:   [u'\u0134',   '.'],   # Jcircumflex
0x02b1:   [u'\u0127',   '.'],   # hstroke
0x02b6:   [u'\u0125',   '.'],   # hcircumflex
0x02b9:   [u'\u0131',   '.'],   # idotless
0x02bb:   [u'\u011f',   '.'],   # gbreve
0x02bc:   [u'\u0135',   '.'],   # jcircumflex
0x02c5:   [u'\u010a',   '.'],   # Cabovedot
0x02c6:   [u'\u0108',   '.'],   # Ccircumflex
0x02d5:   [u'\u0120',   '.'],   # Gabovedot
0x02d8:   [u'\u011c',   '.'],   # Gcircumflex
0x02dd:   [u'\u016c',   '.'],   # Ubreve
0x02de:   [u'\u015c',   '.'],   # Scircumflex
0x02e5:   [u'\u010b',   '.'],   # cabovedot
0x02e6:   [u'\u0109',   '.'],   # ccircumflex
0x02f5:   [u'\u0121',   '.'],   # gabovedot
0x02f8:   [u'\u011d',   '.'],   # gcircumflex
0x02fd:   [u'\u016d',   '.'],   # ubreve
0x02fe:   [u'\u015d',   '.'],   # scircumflex
0x03a2:   [u'\u0138',   '.'],   # kra
0x03a3:   [u'\u0156',   '.'],   # Rcedilla
0x03a5:   [u'\u0128',   '.'],   # Itilde
0x03a6:   [u'\u013b',   '.'],   # Lcedilla
0x03aa:   [u'\u0112',   '.'],   # Emacron
0x03ab:   [u'\u0122',   '.'],   # Gcedilla
0x03ac:   [u'\u0166',   '.'],   # Tslash
0x03b3:   [u'\u0157',   '.'],   # rcedilla
0x03b5:   [u'\u0129',   '.'],   # itilde
0x03b6:   [u'\u013c',   '.'],   # lcedilla
0x03ba:   [u'\u0113',   '.'],   # emacron
0x03bb:   [u'\u0123',   '.'],   # gcedilla
0x03bc:   [u'\u0167',   '.'],   # tslash
0x03bd:   [u'\u014a',   '.'],   # ENG
0x03bf:   [u'\u014b',   '.'],   # eng
0x03c0:   [u'\u0100',   '.'],   # Amacron
0x03c7:   [u'\u012e',   '.'],   # Iogonek
0x03cc:   [u'\u0116',   '.'],   # Eabovedot
0x03cf:   [u'\u012a',   '.'],   # Imacron
0x03d1:   [u'\u0145',   '.'],   # Ncedilla
0x03d2:   [u'\u014c',   '.'],   # Omacron
0x03d3:   [u'\u0136',   '.'],   # Kcedilla
0x03d9:   [u'\u0172',   '.'],   # Uogonek
0x03dd:   [u'\u0168',   '.'],   # Utilde
0x03de:   [u'\u016a',   '.'],   # Umacron
0x03e0:   [u'\u0101',   '.'],   # amacron
0x03e7:   [u'\u012f',   '.'],   # iogonek
0x03ec:   [u'\u0117',   '.'],   # eabovedot
0x03ef:   [u'\u012b',   '.'],   # imacron
0x03f1:   [u'\u0146',   '.'],   # ncedilla
0x03f2:   [u'\u014d',   '.'],   # omacron
0x03f3:   [u'\u0137',   '.'],   # kcedilla
0x03f9:   [u'\u0173',   '.'],   # uogonek
0x03fd:   [u'\u0169',   '.'],   # utilde
0x03fe:   [u'\u016b',   '.'],   # umacron
0x047e:   [u'\u203e',   '.'],   # overline
0x04a1:   [u'\u3002',   '.'],   # kana_fullstop
0x04a2:   [u'\u300c',   '.'],   # kana_openingbracket
0x04a3:   [u'\u300d',   '.'],   # kana_closingbracket
0x04a4:   [u'\u3001',   '.'],   # kana_comma
0x04a5:   [u'\u30fb',   '.'],   # kana_conjunctive
0x04a6:   [u'\u30f2',   '.'],   # kana_WO
0x04a7:   [u'\u30a1',   '.'],   # kana_a
0x04a8:   [u'\u30a3',   '.'],   # kana_i
0x04a9:   [u'\u30a5',   '.'],   # kana_u
0x04aa:   [u'\u30a7',   '.'],   # kana_e
0x04ab:   [u'\u30a9',   '.'],   # kana_o
0x04ac:   [u'\u30e3',   '.'],   # kana_ya
0x04ad:   [u'\u30e5',   '.'],   # kana_yu
0x04ae:   [u'\u30e7',   '.'],   # kana_yo
0x04af:   [u'\u30c3',   '.'],   # kana_tsu
0x04b0:   [u'\u30fc',   '.'],   # prolongedsound
0x04b1:   [u'\u30a2',   '.'],   # kana_A
0x04b2:   [u'\u30a4',   '.'],   # kana_I
0x04b3:   [u'\u30a6',   '.'],   # kana_U
0x04b4:   [u'\u30a8',   '.'],   # kana_E
0x04b5:   [u'\u30aa',   '.'],   # kana_O
0x04b6:   [u'\u30ab',   '.'],   # kana_KA
0x04b7:   [u'\u30ad',   '.'],   # kana_KI
0x04b8:   [u'\u30af',   '.'],   # kana_KU
0x04b9:   [u'\u30b1',   '.'],   # kana_KE
0x04ba:   [u'\u30b3',   '.'],   # kana_KO
0x04bb:   [u'\u30b5',   '.'],   # kana_SA
0x04bc:   [u'\u30b7',   '.'],   # kana_SHI
0x04bd:   [u'\u30b9',   '.'],   # kana_SU
0x04be:   [u'\u30bb',   '.'],   # kana_SE
0x04bf:   [u'\u30bd',   '.'],   # kana_SO
0x04c0:   [u'\u30bf',   '.'],   # kana_TA
0x04c1:   [u'\u30c1',   '.'],   # kana_CHI
0x04c2:   [u'\u30c4',   '.'],   # kana_TSU
0x04c3:   [u'\u30c6',   '.'],   # kana_TE
0x04c4:   [u'\u30c8',   '.'],   # kana_TO
0x04c5:   [u'\u30ca',   '.'],   # kana_NA
0x04c6:   [u'\u30cb',   '.'],   # kana_NI
0x04c7:   [u'\u30cc',   '.'],   # kana_NU
0x04c8:   [u'\u30cd',   '.'],   # kana_NE
0x04c9:   [u'\u30ce',   '.'],   # kana_NO
0x04ca:   [u'\u30cf',   '.'],   # kana_HA
0x04cb:   [u'\u30d2',   '.'],   # kana_HI
0x04cc:   [u'\u30d5',   '.'],   # kana_FU
0x04cd:   [u'\u30d8',   '.'],   # kana_HE
0x04ce:   [u'\u30db',   '.'],   # kana_HO
0x04cf:   [u'\u30de',   '.'],   # kana_MA
0x04d0:   [u'\u30df',   '.'],   # kana_MI
0x04d1:   [u'\u30e0',   '.'],   # kana_MU
0x04d2:   [u'\u30e1',   '.'],   # kana_ME
0x04d3:   [u'\u30e2',   '.'],   # kana_MO
0x04d4:   [u'\u30e4',   '.'],   # kana_YA
0x04d5:   [u'\u30e6',   '.'],   # kana_YU
0x04d6:   [u'\u30e8',   '.'],   # kana_YO
0x04d7:   [u'\u30e9',   '.'],   # kana_RA
0x04d8:   [u'\u30ea',   '.'],   # kana_RI
0x04d9:   [u'\u30eb',   '.'],   # kana_RU
0x04da:   [u'\u30ec',   '.'],   # kana_RE
0x04db:   [u'\u30ed',   '.'],   # kana_RO
0x04dc:   [u'\u30ef',   '.'],   # kana_WA
0x04dd:   [u'\u30f3',   '.'],   # kana_N
0x04de:   [u'\u309b',   '.'],   # voicedsound
0x04df:   [u'\u309c',   '.'],   # semivoicedsound
0x05ac:   [u'\u060c',   '.'],   # Arabic_comma
0x05bb:   [u'\u061b',   '.'],   # Arabic_semicolon
0x05bf:   [u'\u061f',   '.'],   # Arabic_question_mark
0x05c1:   [u'\u0621',   '.'],   # Arabic_hamza
0x05c2:   [u'\u0622',   '.'],   # Arabic_maddaonalef
0x05c3:   [u'\u0623',   '.'],   # Arabic_hamzaonalef
0x05c4:   [u'\u0624',   '.'],   # Arabic_hamzaonwaw
0x05c5:   [u'\u0625',   '.'],   # Arabic_hamzaunderalef
0x05c6:   [u'\u0626',   '.'],   # Arabic_hamzaonyeh
0x05c7:   [u'\u0627',   '.'],   # Arabic_alef
0x05c8:   [u'\u0628',   '.'],   # Arabic_beh
0x05c9:   [u'\u0629',   '.'],   # Arabic_tehmarbuta
0x05ca:   [u'\u062a',   '.'],   # Arabic_teh
0x05cb:   [u'\u062b',   '.'],   # Arabic_theh
0x05cc:   [u'\u062c',   '.'],   # Arabic_jeem
0x05cd:   [u'\u062d',   '.'],   # Arabic_hah
0x05ce:   [u'\u062e',   '.'],   # Arabic_khah
0x05cf:   [u'\u062f',   '.'],   # Arabic_dal
0x05d0:   [u'\u0630',   '.'],   # Arabic_thal
0x05d1:   [u'\u0631',   '.'],   # Arabic_ra
0x05d2:   [u'\u0632',   '.'],   # Arabic_zain
0x05d3:   [u'\u0633',   '.'],   # Arabic_seen
0x05d4:   [u'\u0634',   '.'],   # Arabic_sheen
0x05d5:   [u'\u0635',   '.'],   # Arabic_sad
0x05d6:   [u'\u0636',   '.'],   # Arabic_dad
0x05d7:   [u'\u0637',   '.'],   # Arabic_tah
0x05d8:   [u'\u0638',   '.'],   # Arabic_zah
0x05d9:   [u'\u0639',   '.'],   # Arabic_ain
0x05da:   [u'\u063a',   '.'],   # Arabic_ghain
0x05e0:   [u'\u0640',   '.'],   # Arabic_tatweel
0x05e1:   [u'\u0641',   '.'],   # Arabic_feh
0x05e2:   [u'\u0642',   '.'],   # Arabic_qaf
0x05e3:   [u'\u0643',   '.'],   # Arabic_kaf
0x05e4:   [u'\u0644',   '.'],   # Arabic_lam
0x05e5:   [u'\u0645',   '.'],   # Arabic_meem
0x05e6:   [u'\u0646',   '.'],   # Arabic_noon
0x05e7:   [u'\u0647',   '.'],   # Arabic_ha
0x05e8:   [u'\u0648',   '.'],   # Arabic_waw
0x05e9:   [u'\u0649',   '.'],   # Arabic_alefmaksura
0x05ea:   [u'\u064a',   '.'],   # Arabic_yeh
0x05eb:   [u'\u064b',   '.'],   # Arabic_fathatan
0x05ec:   [u'\u064c',   '.'],   # Arabic_dammatan
0x05ed:   [u'\u064d',   '.'],   # Arabic_kasratan
0x05ee:   [u'\u064e',   '.'],   # Arabic_fatha
0x05ef:   [u'\u064f',   '.'],   # Arabic_damma
0x05f0:   [u'\u0650',   '.'],   # Arabic_kasra
0x05f1:   [u'\u0651',   '.'],   # Arabic_shadda
0x05f2:   [u'\u0652',   '.'],   # Arabic_sukun
0x06a1:   [u'\u0452',   '.'],   # Serbian_dje
0x06a2:   [u'\u0453',   '.'],   # Macedonia_gje
0x06a3:   [u'\u0451',   '.'],   # Cyrillic_io
0x06a4:   [u'\u0454',   '.'],   # Ukrainian_ie
0x06a5:   [u'\u0455',   '.'],   # Macedonia_dse
0x06a6:   [u'\u0456',   '.'],   # Ukrainian_i
0x06a7:   [u'\u0457',   '.'],   # Ukrainian_yi
0x06a8:   [u'\u0458',   '.'],   # Cyrillic_je
0x06a9:   [u'\u0459',   '.'],   # Cyrillic_lje
0x06aa:   [u'\u045a',   '.'],   # Cyrillic_nje
0x06ab:   [u'\u045b',   '.'],   # Serbian_tshe
0x06ac:   [u'\u045c',   '.'],   # Macedonia_kje
0x06ae:   [u'\u045e',   '.'],   # Byelorussian_shortu
0x06af:   [u'\u045f',   '.'],   # Cyrillic_dzhe
0x06b0:   [u'\u2116',   '.'],   # numerosign
0x06b1:   [u'\u0402',   '.'],   # Serbian_DJE
0x06b2:   [u'\u0403',   '.'],   # Macedonia_GJE
0x06b3:   [u'\u0401',   '.'],   # Cyrillic_IO
0x06b4:   [u'\u0404',   '.'],   # Ukrainian_IE
0x06b5:   [u'\u0405',   '.'],   # Macedonia_DSE
0x06b6:   [u'\u0406',   '.'],   # Ukrainian_I
0x06b7:   [u'\u0407',   '.'],   # Ukrainian_YI
0x06b8:   [u'\u0408',   '.'],   # Cyrillic_JE
0x06b9:   [u'\u0409',   '.'],   # Cyrillic_LJE
0x06ba:   [u'\u040a',   '.'],   # Cyrillic_NJE
0x06bb:   [u'\u040b',   '.'],   # Serbian_TSHE
0x06bc:   [u'\u040c',   '.'],   # Macedonia_KJE
0x06be:   [u'\u040e',   '.'],   # Byelorussian_SHORTU
0x06bf:   [u'\u040f',   '.'],   # Cyrillic_DZHE
0x06c0:   [u'\u044e',   '.'],   # Cyrillic_yu
0x06c1:   [u'\u0430',   '.'],   # Cyrillic_a
0x06c2:   [u'\u0431',   '.'],   # Cyrillic_be
0x06c3:   [u'\u0446',   '.'],   # Cyrillic_tse
0x06c4:   [u'\u0434',   '.'],   # Cyrillic_de
0x06c5:   [u'\u0435',   '.'],   # Cyrillic_ie
0x06c6:   [u'\u0444',   '.'],   # Cyrillic_ef
0x06c7:   [u'\u0433',   '.'],   # Cyrillic_ghe
0x06c8:   [u'\u0445',   '.'],   # Cyrillic_ha
0x06c9:   [u'\u0438',   '.'],   # Cyrillic_i
0x06ca:   [u'\u0439',   '.'],   # Cyrillic_shorti
0x06cb:   [u'\u043a',   '.'],   # Cyrillic_ka
0x06cc:   [u'\u043b',   '.'],   # Cyrillic_el
0x06cd:   [u'\u043c',   '.'],   # Cyrillic_em
0x06ce:   [u'\u043d',   '.'],   # Cyrillic_en
0x06cf:   [u'\u043e',   '.'],   # Cyrillic_o
0x06d0:   [u'\u043f',   '.'],   # Cyrillic_pe
0x06d1:   [u'\u044f',   '.'],   # Cyrillic_ya
0x06d2:   [u'\u0440',   '.'],   # Cyrillic_er
0x06d3:   [u'\u0441',   '.'],   # Cyrillic_es
0x06d4:   [u'\u0442',   '.'],   # Cyrillic_te
0x06d5:   [u'\u0443',   '.'],   # Cyrillic_u
0x06d6:   [u'\u0436',   '.'],   # Cyrillic_zhe
0x06d7:   [u'\u0432',   '.'],   # Cyrillic_ve
0x06d8:   [u'\u044c',   '.'],   # Cyrillic_softsign
0x06d9:   [u'\u044b',   '.'],   # Cyrillic_yeru
0x06da:   [u'\u0437',   '.'],   # Cyrillic_ze
0x06db:   [u'\u0448',   '.'],   # Cyrillic_sha
0x06dc:   [u'\u044d',   '.'],   # Cyrillic_e
0x06dd:   [u'\u0449',   '.'],   # Cyrillic_shcha
0x06de:   [u'\u0447',   '.'],   # Cyrillic_che
0x06df:   [u'\u044a',   '.'],   # Cyrillic_hardsign
0x06e0:   [u'\u042e',   '.'],   # Cyrillic_YU
0x06e1:   [u'\u0410',   '.'],   # Cyrillic_A
0x06e2:   [u'\u0411',   '.'],   # Cyrillic_BE
0x06e3:   [u'\u0426',   '.'],   # Cyrillic_TSE
0x06e4:   [u'\u0414',   '.'],   # Cyrillic_DE
0x06e5:   [u'\u0415',   '.'],   # Cyrillic_IE
0x06e6:   [u'\u0424',   '.'],   # Cyrillic_EF
0x06e7:   [u'\u0413',   '.'],   # Cyrillic_GHE
0x06e8:   [u'\u0425',   '.'],   # Cyrillic_HA
0x06e9:   [u'\u0418',   '.'],   # Cyrillic_I
0x06ea:   [u'\u0419',   '.'],   # Cyrillic_SHORTI
0x06eb:   [u'\u041a',   '.'],   # Cyrillic_KA
0x06ec:   [u'\u041b',   '.'],   # Cyrillic_EL
0x06ed:   [u'\u041c',   '.'],   # Cyrillic_EM
0x06ee:   [u'\u041d',   '.'],   # Cyrillic_EN
0x06ef:   [u'\u041e',   '.'],   # Cyrillic_O
0x06f0:   [u'\u041f',   '.'],   # Cyrillic_PE
0x06f1:   [u'\u042f',   '.'],   # Cyrillic_YA
0x06f2:   [u'\u0420',   '.'],   # Cyrillic_ER
0x06f3:   [u'\u0421',   '.'],   # Cyrillic_ES
0x06f4:   [u'\u0422',   '.'],   # Cyrillic_TE
0x06f5:   [u'\u0423',   '.'],   # Cyrillic_U
0x06f6:   [u'\u0416',   '.'],   # Cyrillic_ZHE
0x06f7:   [u'\u0412',   '.'],   # Cyrillic_VE
0x06f8:   [u'\u042c',   '.'],   # Cyrillic_SOFTSIGN
0x06f9:   [u'\u042b',   '.'],   # Cyrillic_YERU
0x06fa:   [u'\u0417',   '.'],   # Cyrillic_ZE
0x06fb:   [u'\u0428',   '.'],   # Cyrillic_SHA
0x06fc:   [u'\u042d',   '.'],   # Cyrillic_E
0x06fd:   [u'\u0429',   '.'],   # Cyrillic_SHCHA
0x06fe:   [u'\u0427',   '.'],   # Cyrillic_CHE
0x06ff:   [u'\u042a',   '.'],   # Cyrillic_HARDSIGN
0x07a1:   [u'\u0386',   '.'],   # Greek_ALPHAaccent
0x07a2:   [u'\u0388',   '.'],   # Greek_EPSILONaccent
0x07a3:   [u'\u0389',   '.'],   # Greek_ETAaccent
0x07a4:   [u'\u038a',   '.'],   # Greek_IOTAaccent
0x07a5:   [u'\u03aa',   '.'],   # Greek_IOTAdiaeresis
0x07a7:   [u'\u038c',   '.'],   # Greek_OMICRONaccent
0x07a8:   [u'\u038e',   '.'],   # Greek_UPSILONaccent
0x07a9:   [u'\u03ab',   '.'],   # Greek_UPSILONdieresis
0x07ab:   [u'\u038f',   '.'],   # Greek_OMEGAaccent
0x07ae:   [u'\u0385',   '.'],   # Greek_accentdieresis
0x07af:   [u'\u2015',   '.'],   # Greek_horizbar
0x07b1:   [u'\u03ac',   '.'],   # Greek_alphaaccent
0x07b2:   [u'\u03ad',   '.'],   # Greek_epsilonaccent
0x07b3:   [u'\u03ae',   '.'],   # Greek_etaaccent
0x07b4:   [u'\u03af',   '.'],   # Greek_iotaaccent
0x07b5:   [u'\u03ca',   '.'],   # Greek_iotadieresis
0x07b6:   [u'\u0390',   '.'],   # Greek_iotaaccentdieresis
0x07b7:   [u'\u03cc',   '.'],   # Greek_omicronaccent
0x07b8:   [u'\u03cd',   '.'],   # Greek_upsilonaccent
0x07b9:   [u'\u03cb',   '.'],   # Greek_upsilondieresis
0x07ba:   [u'\u03b0',   '.'],   # Greek_upsilonaccentdieresis
0x07bb:   [u'\u03ce',   '.'],   # Greek_omegaaccent
0x07c1:   [u'\u0391',   '.'],   # Greek_ALPHA
0x07c2:   [u'\u0392',   '.'],   # Greek_BETA
0x07c3:   [u'\u0393',   '.'],   # Greek_GAMMA
0x07c4:   [u'\u0394',   '.'],   # Greek_DELTA
0x07c5:   [u'\u0395',   '.'],   # Greek_EPSILON
0x07c6:   [u'\u0396',   '.'],   # Greek_ZETA
0x07c7:   [u'\u0397',   '.'],   # Greek_ETA
0x07c8:   [u'\u0398',   '.'],   # Greek_THETA
0x07c9:   [u'\u0399',   '.'],   # Greek_IOTA
0x07ca:   [u'\u039a',   '.'],   # Greek_KAPPA
0x07cb:   [u'\u039b',   '.'],   # Greek_LAMBDA
0x07cb:   [u'\u039b',   '.'],   # Greek_LAMDA
0x07cc:   [u'\u039c',   '.'],   # Greek_MU
0x07cd:   [u'\u039d',   '.'],   # Greek_NU
0x07ce:   [u'\u039e',   '.'],   # Greek_XI
0x07cf:   [u'\u039f',   '.'],   # Greek_OMICRON
0x07d0:   [u'\u03a0',   '.'],   # Greek_PI
0x07d1:   [u'\u03a1',   '.'],   # Greek_RHO
0x07d2:   [u'\u03a3',   '.'],   # Greek_SIGMA
0x07d4:   [u'\u03a4',   '.'],   # Greek_TAU
0x07d5:   [u'\u03a5',   '.'],   # Greek_UPSILON
0x07d6:   [u'\u03a6',   '.'],   # Greek_PHI
0x07d7:   [u'\u03a7',   '.'],   # Greek_CHI
0x07d8:   [u'\u03a8',   '.'],   # Greek_PSI
0x07d9:   [u'\u03a9',   '.'],   # Greek_OMEGA
0x07e1:   [u'\u03b1',   '.'],   # Greek_alpha
0x07e2:   [u'\u03b2',   '.'],   # Greek_beta
0x07e3:   [u'\u03b3',   '.'],   # Greek_gamma
0x07e4:   [u'\u03b4',   '.'],   # Greek_delta
0x07e5:   [u'\u03b5',   '.'],   # Greek_epsilon
0x07e6:   [u'\u03b6',   '.'],   # Greek_zeta
0x07e7:   [u'\u03b7',   '.'],   # Greek_eta
0x07e8:   [u'\u03b8',   '.'],   # Greek_theta
0x07e9:   [u'\u03b9',   '.'],   # Greek_iota
0x07ea:   [u'\u03ba',   '.'],   # Greek_kappa
0x07eb:   [u'\u03bb',   '.'],   # Greek_lambda
0x07ec:   [u'\u03bc',   '.'],   # Greek_mu
0x07ed:   [u'\u03bd',   '.'],   # Greek_nu
0x07ee:   [u'\u03be',   '.'],   # Greek_xi
0x07ef:   [u'\u03bf',   '.'],   # Greek_omicron
0x07f0:   [u'\u03c0',   '.'],   # Greek_pi
0x07f1:   [u'\u03c1',   '.'],   # Greek_rho
0x07f2:   [u'\u03c3',   '.'],   # Greek_sigma
0x07f3:   [u'\u03c2',   '.'],   # Greek_finalsmallsigma
0x07f4:   [u'\u03c4',   '.'],   # Greek_tau
0x07f5:   [u'\u03c5',   '.'],   # Greek_upsilon
0x07f6:   [u'\u03c6',   '.'],   # Greek_phi
0x07f7:   [u'\u03c7',   '.'],   # Greek_chi
0x07f8:   [u'\u03c8',   '.'],   # Greek_psi
0x07f9:   [u'\u03c9',   '.'],   # Greek_omega
0x08a1:   [u'\u23b7',   '.'],   # leftradical
0x08a2:   [u'\u250c',   'd'],   # topleftradical
0x08a3:   [u'\u2500',   'd'],   # horizconnector
0x08a4:   [u'\u2320',   '.'],   # topintegral
0x08a5:   [u'\u2321',   '.'],   # botintegral
0x08a6:   [u'\u2502',   'd'],   # vertconnector
0x08a7:   [u'\u23a1',   '.'],   # topleftsqbracket
0x08a8:   [u'\u23a3',   '.'],   # botleftsqbracket
0x08a9:   [u'\u23a4',   '.'],   # toprightsqbracket
0x08aa:   [u'\u23a6',   '.'],   # botrightsqbracket
0x08ab:   [u'\u239b',   '.'],   # topleftparens
0x08ac:   [u'\u239d',   '.'],   # botleftparens
0x08ad:   [u'\u239e',   '.'],   # toprightparens
0x08ae:   [u'\u23a0',   '.'],   # botrightparens
0x08af:   [u'\u23a8',   '.'],   # leftmiddlecurlybrace
0x08b0:   [u'\u23ac',   '.'],   # rightmiddlecurlybrace
0x08b1:   [None     ,   'o'],   # topleftsummation
0x08b2:   [None     ,   'o'],   # botleftsummation
0x08b3:   [None     ,   'o'],   # topvertsummationconnector
0x08b4:   [None     ,   'o'],   # botvertsummationconnector
0x08b5:   [None     ,   'o'],   # toprightsummation
0x08b6:   [None     ,   'o'],   # botrightsummation
0x08b7:   [None     ,   'o'],   # rightmiddlesummation
0x08bc:   [u'\u2264',   '.'],   # lessthanequal
0x08bd:   [u'\u2260',   '.'],   # notequal
0x08be:   [u'\u2265',   '.'],   # greaterthanequal
0x08bf:   [u'\u222b',   '.'],   # integral
0x08c0:   [u'\u2234',   '.'],   # therefore
0x08c1:   [u'\u221d',   '.'],   # variation
0x08c2:   [u'\u221e',   '.'],   # infinity
0x08c5:   [u'\u2207',   '.'],   # nabla
0x08c8:   [u'\u223c',   '.'],   # approximate
0x08c9:   [u'\u2243',   '.'],   # similarequal
0x08cd:   [u'\u21d4',   '.'],   # ifonlyif
0x08ce:   [u'\u21d2',   '.'],   # implies
0x08cf:   [u'\u2261',   '.'],   # identical
0x08d6:   [u'\u221a',   '.'],   # radical
0x08da:   [u'\u2282',   '.'],   # includedin
0x08db:   [u'\u2283',   '.'],   # includes
0x08dc:   [u'\u2229',   '.'],   # intersection
0x08dd:   [u'\u222a',   '.'],   # union
0x08de:   [u'\u2227',   '.'],   # logicaland
0x08df:   [u'\u2228',   '.'],   # logicalor
0x08ef:   [u'\u2202',   '.'],   # partialderivative
0x08f6:   [u'\u0192',   '.'],   # function
0x08fb:   [u'\u2190',   '.'],   # leftarrow
0x08fc:   [u'\u2191',   '.'],   # uparrow
0x08fd:   [u'\u2192',   '.'],   # rightarrow
0x08fe:   [u'\u2193',   '.'],   # downarrow
0x09df:   [None     ,   'o'],   # blank
0x09e0:   [u'\u25c6',   '.'],   # soliddiamond
0x09e1:   [u'\u2592',   '.'],   # checkerboard
0x09e2:   [u'\u2409',   '.'],   # ht
0x09e3:   [u'\u240c',   '.'],   # ff
0x09e4:   [u'\u240d',   '.'],   # cr
0x09e5:   [u'\u240a',   '.'],   # lf
0x09e8:   [u'\u2424',   '.'],   # nl
0x09e9:   [u'\u240b',   '.'],   # vt
0x09ea:   [u'\u2518',   '.'],   # lowrightcorner
0x09eb:   [u'\u2510',   '.'],   # uprightcorner
0x09ec:   [u'\u250c',   '.'],   # upleftcorner
0x09ed:   [u'\u2514',   '.'],   # lowleftcorner
0x09ee:   [u'\u253c',   '.'],   # crossinglines
0x09ef:   [u'\u23ba',   '.'],   # horizlinescan1
0x09f0:   [u'\u23bb',   '.'],   # horizlinescan3
0x09f1:   [u'\u2500',   '.'],   # horizlinescan5
0x09f2:   [u'\u23bc',   '.'],   # horizlinescan7
0x09f3:   [u'\u23bd',   '.'],   # horizlinescan9
0x09f4:   [u'\u251c',   '.'],   # leftt
0x09f5:   [u'\u2524',   '.'],   # rightt
0x09f6:   [u'\u2534',   '.'],   # bott
0x09f7:   [u'\u252c',   '.'],   # topt
0x09f8:   [u'\u2502',   '.'],   # vertbar
0x0aa1:   [u'\u2003',   '.'],   # emspace
0x0aa2:   [u'\u2002',   '.'],   # enspace
0x0aa3:   [u'\u2004',   '.'],   # em3space
0x0aa4:   [u'\u2005',   '.'],   # em4space
0x0aa5:   [u'\u2007',   '.'],   # digitspace
0x0aa6:   [u'\u2008',   '.'],   # punctspace
0x0aa7:   [u'\u2009',   '.'],   # thinspace
0x0aa8:   [u'\u200a',   '.'],   # hairspace
0x0aa9:   [u'\u2014',   '.'],   # emdash
0x0aaa:   [u'\u2013',   '.'],   # endash
0x0aac:   [u'\u2423',   'o'],   # signifblank
0x0aae:   [u'\u2026',   '.'],   # ellipsis
0x0aaf:   [u'\u2025',   '.'],   # doubbaselinedot
0x0ab0:   [u'\u2153',   '.'],   # onethird
0x0ab1:   [u'\u2154',   '.'],   # twothirds
0x0ab2:   [u'\u2155',   '.'],   # onefifth
0x0ab3:   [u'\u2156',   '.'],   # twofifths
0x0ab4:   [u'\u2157',   '.'],   # threefifths
0x0ab5:   [u'\u2158',   '.'],   # fourfifths
0x0ab6:   [u'\u2159',   '.'],   # onesixth
0x0ab7:   [u'\u215a',   '.'],   # fivesixths
0x0ab8:   [u'\u2105',   '.'],   # careof
0x0abb:   [u'\u2012',   '.'],   # figdash
0x0abc:   [u'\u27e8',   'o'],   # leftanglebracket
0x0abd:   [u'\u002e',   'o'],   # decimalpoint
0x0abe:   [u'\u27e9',   'o'],   # rightanglebracket
0x0abf:   [None     ,   'o'],   # marker
0x0ac3:   [u'\u215b',   '.'],   # oneeighth
0x0ac4:   [u'\u215c',   '.'],   # threeeighths
0x0ac5:   [u'\u215d',   '.'],   # fiveeighths
0x0ac6:   [u'\u215e',   '.'],   # seveneighths
0x0ac9:   [u'\u2122',   '.'],   # trademark
0x0aca:   [u'\u2613',   'o'],   # signaturemark
0x0acb:   [None     ,   'o'],   # trademarkincircle
0x0acc:   [u'\u25c1',   'o'],   # leftopentriangle
0x0acd:   [u'\u25b7',   'o'],   # rightopentriangle
0x0ace:   [u'\u25cb',   'o'],   # emopencircle
0x0acf:   [u'\u25af',   'o'],   # emopenrectangle
0x0ad0:   [u'\u2018',   '.'],   # leftsinglequotemark
0x0ad1:   [u'\u2019',   '.'],   # rightsinglequotemark
0x0ad2:   [u'\u201c',   '.'],   # leftdoublequotemark
0x0ad3:   [u'\u201d',   '.'],   # rightdoublequotemark
0x0ad4:   [u'\u211e',   '.'],   # prescription
0x0ad6:   [u'\u2032',   '.'],   # minutes
0x0ad7:   [u'\u2033',   '.'],   # seconds
0x0ad9:   [u'\u271d',   '.'],   # latincross
0x0ada:   [None     ,   'o'],   # hexagram
0x0adb:   [u'\u25ac',   'o'],   # filledrectbullet
0x0adc:   [u'\u25c0',   'o'],   # filledlefttribullet
0x0add:   [u'\u25b6',   'o'],   # filledrighttribullet
0x0ade:   [u'\u25cf',   'o'],   # emfilledcircle
0x0adf:   [u'\u25ae',   'o'],   # emfilledrect
0x0ae0:   [u'\u25e6',   'o'],   # enopencircbullet
0x0ae1:   [u'\u25ab',   'o'],   # enopensquarebullet
0x0ae2:   [u'\u25ad',   'o'],   # openrectbullet
0x0ae3:   [u'\u25b3',   'o'],   # opentribulletup
0x0ae4:   [u'\u25bd',   'o'],   # opentribulletdown
0x0ae5:   [u'\u2606',   'o'],   # openstar
0x0ae6:   [u'\u2022',   'o'],   # enfilledcircbullet
0x0ae7:   [u'\u25aa',   'o'],   # enfilledsqbullet
0x0ae8:   [u'\u25b2',   'o'],   # filledtribulletup
0x0ae9:   [u'\u25bc',   'o'],   # filledtribulletdown
0x0aea:   [u'\u261c',   'o'],   # leftpointer
0x0aeb:   [u'\u261e',   'o'],   # rightpointer
0x0aec:   [u'\u2663',   '.'],   # club
0x0aed:   [u'\u2666',   '.'],   # diamond
0x0aee:   [u'\u2665',   '.'],   # heart
0x0af0:   [u'\u2720',   '.'],   # maltesecross
0x0af1:   [u'\u2020',   '.'],   # dagger
0x0af2:   [u'\u2021',   '.'],   # doubledagger
0x0af3:   [u'\u2713',   '.'],   # checkmark
0x0af4:   [u'\u2717',   '.'],   # ballotcross
0x0af5:   [u'\u266f',   '.'],   # musicalsharp
0x0af6:   [u'\u266d',   '.'],   # musicalflat
0x0af7:   [u'\u2642',   '.'],   # malesymbol
0x0af8:   [u'\u2640',   '.'],   # femalesymbol
0x0af9:   [u'\u260e',   '.'],   # telephone
0x0afa:   [u'\u2315',   '.'],   # telephonerecorder
0x0afb:   [u'\u2117',   '.'],   # phonographcopyright
0x0afc:   [u'\u2038',   '.'],   # caret
0x0afd:   [u'\u201a',   '.'],   # singlelowquotemark
0x0afe:   [u'\u201e',   '.'],   # doublelowquotemark
0x0aff:   [None     ,   'o'],   # cursor
0x0ba3:   [u'\u003c',   'd'],   # leftcaret
0x0ba6:   [u'\u003e',   'd'],   # rightcaret
0x0ba8:   [u'\u2228',   'd'],   # downcaret
0x0ba9:   [u'\u2227',   'd'],   # upcaret
0x0bc0:   [u'\u00af',   'd'],   # overbar
0x0bc2:   [u'\u22a5',   '.'],   # downtack
0x0bc3:   [u'\u2229',   'd'],   # upshoe
0x0bc4:   [u'\u230a',   '.'],   # downstile
0x0bc6:   [u'\u005f',   'd'],   # underbar
0x0bca:   [u'\u2218',   '.'],   # jot
0x0bcc:   [u'\u2395',   '.'],   # quad
0x0bce:   [u'\u22a4',   '.'],   # uptack
0x0bcf:   [u'\u25cb',   '.'],   # circle
0x0bd3:   [u'\u2308',   '.'],   # upstile
0x0bd6:   [u'\u222a',   'd'],   # downshoe
0x0bd8:   [u'\u2283',   'd'],   # rightshoe
0x0bda:   [u'\u2282',   'd'],   # leftshoe
0x0bdc:   [u'\u22a2',   '.'],   # lefttack
0x0bfc:   [u'\u22a3',   '.'],   # righttack
0x0cdf:   [u'\u2017',   '.'],   # hebrew_doublelowline
0x0ce0:   [u'\u05d0',   '.'],   # hebrew_aleph
0x0ce1:   [u'\u05d1',   '.'],   # hebrew_bet
0x0ce1:   [u'\u05d1',   '.'],   # hebrew_beth  /* deprecated */
0x0ce2:   [u'\u05d2',   '.'],   # hebrew_gimel
0x0ce2:   [u'\u05d2',   '.'],   # hebrew_gimmel  /* deprecated */
0x0ce3:   [u'\u05d3',   '.'],   # hebrew_dalet
0x0ce3:   [u'\u05d3',   '.'],   # hebrew_daleth  /* deprecated */
0x0ce4:   [u'\u05d4',   '.'],   # hebrew_he
0x0ce5:   [u'\u05d5',   '.'],   # hebrew_waw
0x0ce6:   [u'\u05d6',   '.'],   # hebrew_zain
0x0ce6:   [u'\u05d6',   '.'],   # hebrew_zayin  /* deprecated */
0x0ce7:   [u'\u05d7',   '.'],   # hebrew_chet
0x0ce7:   [u'\u05d7',   '.'],   # hebrew_het  /* deprecated */
0x0ce8:   [u'\u05d8',   '.'],   # hebrew_tet
0x0ce8:   [u'\u05d8',   '.'],   # hebrew_teth  /* deprecated */
0x0ce9:   [u'\u05d9',   '.'],   # hebrew_yod
0x0cea:   [u'\u05da',   '.'],   # hebrew_finalkaph
0x0ceb:   [u'\u05db',   '.'],   # hebrew_kaph
0x0cec:   [u'\u05dc',   '.'],   # hebrew_lamed
0x0ced:   [u'\u05dd',   '.'],   # hebrew_finalmem
0x0cee:   [u'\u05de',   '.'],   # hebrew_mem
0x0cef:   [u'\u05df',   '.'],   # hebrew_finalnun
0x0cf0:   [u'\u05e0',   '.'],   # hebrew_nun
0x0cf1:   [u'\u05e1',   '.'],   # hebrew_samech
0x0cf1:   [u'\u05e1',   '.'],   # hebrew_samekh  /* deprecated */
0x0cf2:   [u'\u05e2',   '.'],   # hebrew_ayin
0x0cf3:   [u'\u05e3',   '.'],   # hebrew_finalpe
0x0cf4:   [u'\u05e4',   '.'],   # hebrew_pe
0x0cf5:   [u'\u05e5',   '.'],   # hebrew_finalzade
0x0cf5:   [u'\u05e5',   '.'],   # hebrew_finalzadi  /* deprecated */
0x0cf6:   [u'\u05e6',   '.'],   # hebrew_zade
0x0cf6:   [u'\u05e6',   '.'],   # hebrew_zadi  /* deprecated */
0x0cf7:   [u'\u05e7',   '.'],   # hebrew_kuf  /* deprecated */
0x0cf7:   [u'\u05e7',   '.'],   # hebrew_qoph
0x0cf8:   [u'\u05e8',   '.'],   # hebrew_resh
0x0cf9:   [u'\u05e9',   '.'],   # hebrew_shin
0x0cfa:   [u'\u05ea',   '.'],   # hebrew_taf  /* deprecated */
0x0cfa:   [u'\u05ea',   '.'],   # hebrew_taw
0x0da1:   [u'\u0e01',   '.'],   # Thai_kokai
0x0da2:   [u'\u0e02',   '.'],   # Thai_khokhai
0x0da3:   [u'\u0e03',   '.'],   # Thai_khokhuat
0x0da4:   [u'\u0e04',   '.'],   # Thai_khokhwai
0x0da5:   [u'\u0e05',   '.'],   # Thai_khokhon
0x0da6:   [u'\u0e06',   '.'],   # Thai_khorakhang
0x0da7:   [u'\u0e07',   '.'],   # Thai_ngongu
0x0da8:   [u'\u0e08',   '.'],   # Thai_chochan
0x0da9:   [u'\u0e09',   '.'],   # Thai_choching
0x0daa:   [u'\u0e0a',   '.'],   # Thai_chochang
0x0dab:   [u'\u0e0b',   '.'],   # Thai_soso
0x0dac:   [u'\u0e0c',   '.'],   # Thai_chochoe
0x0dad:   [u'\u0e0d',   '.'],   # Thai_yoying
0x0dae:   [u'\u0e0e',   '.'],   # Thai_dochada
0x0daf:   [u'\u0e0f',   '.'],   # Thai_topatak
0x0db0:   [u'\u0e10',   '.'],   # Thai_thothan
0x0db1:   [u'\u0e11',   '.'],   # Thai_thonangmontho
0x0db2:   [u'\u0e12',   '.'],   # Thai_thophuthao
0x0db3:   [u'\u0e13',   '.'],   # Thai_nonen
0x0db4:   [u'\u0e14',   '.'],   # Thai_dodek
0x0db5:   [u'\u0e15',   '.'],   # Thai_totao
0x0db6:   [u'\u0e16',   '.'],   # Thai_thothung
0x0db7:   [u'\u0e17',   '.'],   # Thai_thothahan
0x0db8:   [u'\u0e18',   '.'],   # Thai_thothong
0x0db9:   [u'\u0e19',   '.'],   # Thai_nonu
0x0dba:   [u'\u0e1a',   '.'],   # Thai_bobaimai
0x0dbb:   [u'\u0e1b',   '.'],   # Thai_popla
0x0dbc:   [u'\u0e1c',   '.'],   # Thai_phophung
0x0dbd:   [u'\u0e1d',   '.'],   # Thai_fofa
0x0dbe:   [u'\u0e1e',   '.'],   # Thai_phophan
0x0dbf:   [u'\u0e1f',   '.'],   # Thai_fofan
0x0dc0:   [u'\u0e20',   '.'],   # Thai_phosamphao
0x0dc1:   [u'\u0e21',   '.'],   # Thai_moma
0x0dc2:   [u'\u0e22',   '.'],   # Thai_yoyak
0x0dc3:   [u'\u0e23',   '.'],   # Thai_rorua
0x0dc4:   [u'\u0e24',   '.'],   # Thai_ru
0x0dc5:   [u'\u0e25',   '.'],   # Thai_loling
0x0dc6:   [u'\u0e26',   '.'],   # Thai_lu
0x0dc7:   [u'\u0e27',   '.'],   # Thai_wowaen
0x0dc8:   [u'\u0e28',   '.'],   # Thai_sosala
0x0dc9:   [u'\u0e29',   '.'],   # Thai_sorusi
0x0dca:   [u'\u0e2a',   '.'],   # Thai_sosua
0x0dcb:   [u'\u0e2b',   '.'],   # Thai_hohip
0x0dcc:   [u'\u0e2c',   '.'],   # Thai_lochula
0x0dcd:   [u'\u0e2d',   '.'],   # Thai_oang
0x0dce:   [u'\u0e2e',   '.'],   # Thai_honokhuk
0x0dcf:   [u'\u0e2f',   '.'],   # Thai_paiyannoi
0x0dd0:   [u'\u0e30',   '.'],   # Thai_saraa
0x0dd1:   [u'\u0e31',   '.'],   # Thai_maihanakat
0x0dd2:   [u'\u0e32',   '.'],   # Thai_saraaa
0x0dd3:   [u'\u0e33',   '.'],   # Thai_saraam
0x0dd4:   [u'\u0e34',   '.'],   # Thai_sarai
0x0dd5:   [u'\u0e35',   '.'],   # Thai_saraii
0x0dd6:   [u'\u0e36',   '.'],   # Thai_saraue
0x0dd7:   [u'\u0e37',   '.'],   # Thai_sarauee
0x0dd8:   [u'\u0e38',   '.'],   # Thai_sarau
0x0dd9:   [u'\u0e39',   '.'],   # Thai_sarauu
0x0dda:   [u'\u0e3a',   '.'],   # Thai_phinthu
0x0dde:   [None     ,   'o'],   # Thai_maihanakat_maitho
0x0ddf:   [u'\u0e3f',   '.'],   # Thai_baht
0x0de0:   [u'\u0e40',   '.'],   # Thai_sarae
0x0de1:   [u'\u0e41',   '.'],   # Thai_saraae
0x0de2:   [u'\u0e42',   '.'],   # Thai_sarao
0x0de3:   [u'\u0e43',   '.'],   # Thai_saraaimaimuan
0x0de4:   [u'\u0e44',   '.'],   # Thai_saraaimaimalai
0x0de5:   [u'\u0e45',   '.'],   # Thai_lakkhangyao
0x0de6:   [u'\u0e46',   '.'],   # Thai_maiyamok
0x0de7:   [u'\u0e47',   '.'],   # Thai_maitaikhu
0x0de8:   [u'\u0e48',   '.'],   # Thai_maiek
0x0de9:   [u'\u0e49',   '.'],   # Thai_maitho
0x0dea:   [u'\u0e4a',   '.'],   # Thai_maitri
0x0deb:   [u'\u0e4b',   '.'],   # Thai_maichattawa
0x0dec:   [u'\u0e4c',   '.'],   # Thai_thanthakhat
0x0ded:   [u'\u0e4d',   '.'],   # Thai_nikhahit
0x0df0:   [u'\u0e50',   '.'],   # Thai_leksun
0x0df1:   [u'\u0e51',   '.'],   # Thai_leknung
0x0df2:   [u'\u0e52',   '.'],   # Thai_leksong
0x0df3:   [u'\u0e53',   '.'],   # Thai_leksam
0x0df4:   [u'\u0e54',   '.'],   # Thai_leksi
0x0df5:   [u'\u0e55',   '.'],   # Thai_lekha
0x0df6:   [u'\u0e56',   '.'],   # Thai_lekhok
0x0df7:   [u'\u0e57',   '.'],   # Thai_lekchet
0x0df8:   [u'\u0e58',   '.'],   # Thai_lekpaet
0x0df9:   [u'\u0e59',   '.'],   # Thai_lekkao
0x0ea1:   [u'\u3131',   'f'],   # Hangul_Kiyeog
0x0ea2:   [u'\u3132',   'f'],   # Hangul_SsangKiyeog
0x0ea3:   [u'\u3133',   'f'],   # Hangul_KiyeogSios
0x0ea4:   [u'\u3134',   'f'],   # Hangul_Nieun
0x0ea5:   [u'\u3135',   'f'],   # Hangul_NieunJieuj
0x0ea6:   [u'\u3136',   'f'],   # Hangul_NieunHieuh
0x0ea7:   [u'\u3137',   'f'],   # Hangul_Dikeud
0x0ea8:   [u'\u3138',   'f'],   # Hangul_SsangDikeud
0x0ea9:   [u'\u3139',   'f'],   # Hangul_Rieul
0x0eaa:   [u'\u313a',   'f'],   # Hangul_RieulKiyeog
0x0eab:   [u'\u313b',   'f'],   # Hangul_RieulMieum
0x0eac:   [u'\u313c',   'f'],   # Hangul_RieulPieub
0x0ead:   [u'\u313d',   'f'],   # Hangul_RieulSios
0x0eae:   [u'\u313e',   'f'],   # Hangul_RieulTieut
0x0eaf:   [u'\u313f',   'f'],   # Hangul_RieulPhieuf
0x0eb0:   [u'\u3140',   'f'],   # Hangul_RieulHieuh
0x0eb1:   [u'\u3141',   'f'],   # Hangul_Mieum
0x0eb2:   [u'\u3142',   'f'],   # Hangul_Pieub
0x0eb3:   [u'\u3143',   'f'],   # Hangul_SsangPieub
0x0eb4:   [u'\u3144',   'f'],   # Hangul_PieubSios
0x0eb5:   [u'\u3145',   'f'],   # Hangul_Sios
0x0eb6:   [u'\u3146',   'f'],   # Hangul_SsangSios
0x0eb7:   [u'\u3147',   'f'],   # Hangul_Ieung
0x0eb8:   [u'\u3148',   'f'],   # Hangul_Jieuj
0x0eb9:   [u'\u3149',   'f'],   # Hangul_SsangJieuj
0x0eba:   [u'\u314a',   'f'],   # Hangul_Cieuc
0x0ebb:   [u'\u314b',   'f'],   # Hangul_Khieuq
0x0ebc:   [u'\u314c',   'f'],   # Hangul_Tieut
0x0ebd:   [u'\u314d',   'f'],   # Hangul_Phieuf
0x0ebe:   [u'\u314e',   'f'],   # Hangul_Hieuh
0x0ebf:   [u'\u314f',   'f'],   # Hangul_A
0x0ec0:   [u'\u3150',   'f'],   # Hangul_AE
0x0ec1:   [u'\u3151',   'f'],   # Hangul_YA
0x0ec2:   [u'\u3152',   'f'],   # Hangul_YAE
0x0ec3:   [u'\u3153',   'f'],   # Hangul_EO
0x0ec4:   [u'\u3154',   'f'],   # Hangul_E
0x0ec5:   [u'\u3155',   'f'],   # Hangul_YEO
0x0ec6:   [u'\u3156',   'f'],   # Hangul_YE
0x0ec7:   [u'\u3157',   'f'],   # Hangul_O
0x0ec8:   [u'\u3158',   'f'],   # Hangul_WA
0x0ec9:   [u'\u3159',   'f'],   # Hangul_WAE
0x0eca:   [u'\u315a',   'f'],   # Hangul_OE
0x0ecb:   [u'\u315b',   'f'],   # Hangul_YO
0x0ecc:   [u'\u315c',   'f'],   # Hangul_U
0x0ecd:   [u'\u315d',   'f'],   # Hangul_WEO
0x0ece:   [u'\u315e',   'f'],   # Hangul_WE
0x0ecf:   [u'\u315f',   'f'],   # Hangul_WI
0x0ed0:   [u'\u3160',   'f'],   # Hangul_YU
0x0ed1:   [u'\u3161',   'f'],   # Hangul_EU
0x0ed2:   [u'\u3162',   'f'],   # Hangul_YI
0x0ed3:   [u'\u3163',   'f'],   # Hangul_I
0x0ed4:   [u'\u11a8',   'f'],   # Hangul_J_Kiyeog
0x0ed5:   [u'\u11a9',   'f'],   # Hangul_J_SsangKiyeog
0x0ed6:   [u'\u11aa',   'f'],   # Hangul_J_KiyeogSios
0x0ed7:   [u'\u11ab',   'f'],   # Hangul_J_Nieun
0x0ed8:   [u'\u11ac',   'f'],   # Hangul_J_NieunJieuj
0x0ed9:   [u'\u11ad',   'f'],   # Hangul_J_NieunHieuh
0x0eda:   [u'\u11ae',   'f'],   # Hangul_J_Dikeud
0x0edb:   [u'\u11af',   'f'],   # Hangul_J_Rieul
0x0edc:   [u'\u11b0',   'f'],   # Hangul_J_RieulKiyeog
0x0edd:   [u'\u11b1',   'f'],   # Hangul_J_RieulMieum
0x0ede:   [u'\u11b2',   'f'],   # Hangul_J_RieulPieub
0x0edf:   [u'\u11b3',   'f'],   # Hangul_J_RieulSios
0x0ee0:   [u'\u11b4',   'f'],   # Hangul_J_RieulTieut
0x0ee1:   [u'\u11b5',   'f'],   # Hangul_J_RieulPhieuf
0x0ee2:   [u'\u11b6',   'f'],   # Hangul_J_RieulHieuh
0x0ee3:   [u'\u11b7',   'f'],   # Hangul_J_Mieum
0x0ee4:   [u'\u11b8',   'f'],   # Hangul_J_Pieub
0x0ee5:   [u'\u11b9',   'f'],   # Hangul_J_PieubSios
0x0ee6:   [u'\u11ba',   'f'],   # Hangul_J_Sios
0x0ee7:   [u'\u11bb',   'f'],   # Hangul_J_SsangSios
0x0ee8:   [u'\u11bc',   'f'],   # Hangul_J_Ieung
0x0ee9:   [u'\u11bd',   'f'],   # Hangul_J_Jieuj
0x0eea:   [u'\u11be',   'f'],   # Hangul_J_Cieuc
0x0eeb:   [u'\u11bf',   'f'],   # Hangul_J_Khieuq
0x0eec:   [u'\u11c0',   'f'],   # Hangul_J_Tieut
0x0eed:   [u'\u11c1',   'f'],   # Hangul_J_Phieuf
0x0eee:   [u'\u11c2',   'f'],   # Hangul_J_Hieuh
0x0eef:   [u'\u316d',   'f'],   # Hangul_RieulYeorinHieuh
0x0ef0:   [u'\u3171',   'f'],   # Hangul_SunkyeongeumMieum
0x0ef1:   [u'\u3178',   'f'],   # Hangul_SunkyeongeumPieub
0x0ef2:   [u'\u317f',   'f'],   # Hangul_PanSios
0x0ef3:   [u'\u3181',   'f'],   # Hangul_KkogjiDalrinIeung
0x0ef4:   [u'\u3184',   'f'],   # Hangul_SunkyeongeumPhieuf
0x0ef5:   [u'\u3186',   'f'],   # Hangul_YeorinHieuh
0x0ef6:   [u'\u318d',   'f'],   # Hangul_AraeA
0x0ef7:   [u'\u318e',   'f'],   # Hangul_AraeAE
0x0ef8:   [u'\u11eb',   'f'],   # Hangul_J_PanSios
0x0ef9:   [u'\u11f0',   'f'],   # Hangul_J_KkogjiDalrinIeung
0x0efa:   [u'\u11f9',   'f'],   # Hangul_J_YeorinHieuh
0x0eff:   [u'\u20a9',   'o'],   # Korean_Won
0x13bc:   [u'\u0152',   '.'],   # OE
0x13bd:   [u'\u0153',   '.'],   # oe
0x13be:   [u'\u0178',   '.'],   # Ydiaeresis
0x20a0:   [u'\u20a0',   'u'],   # EcuSign
0x20a1:   [u'\u20a1',   'u'],   # ColonSign
0x20a2:   [u'\u20a2',   'u'],   # CruzeiroSign
0x20a3:   [u'\u20a3',   'u'],   # FFrancSign
0x20a4:   [u'\u20a4',   'u'],   # LiraSign
0x20a5:   [u'\u20a5',   'u'],   # MillSign
0x20a6:   [u'\u20a6',   'u'],   # NairaSign
0x20a7:   [u'\u20a7',   'u'],   # PesetaSign
0x20a8:   [u'\u20a8',   'u'],   # RupeeSign
0x20a9:   [u'\u20a9',   'u'],   # WonSign
0x20aa:   [u'\u20aa',   'u'],   # NewSheqelSign
0x20ab:   [u'\u20ab',   'u'],   # DongSign
0x20ac:   [u'\u20ac',   '.'],   # EuroSign
0xfd01:   [None     ,   'f'],   # 3270_Duplicate
0xfd02:   [None     ,   'f'],   # 3270_FieldMark
0xfd03:   [None     ,   'f'],   # 3270_Right2
0xfd04:   [None     ,   'f'],   # 3270_Left2
0xfd05:   [None     ,   'f'],   # 3270_BackTab
0xfd06:   [None     ,   'f'],   # 3270_EraseEOF
0xfd07:   [None     ,   'f'],   # 3270_EraseInput
0xfd08:   [None     ,   'f'],   # 3270_Reset
0xfd09:   [None     ,   'f'],   # 3270_Quit
0xfd0a:   [None     ,   'f'],   # 3270_PA1
0xfd0b:   [None     ,   'f'],   # 3270_PA2
0xfd0c:   [None     ,   'f'],   # 3270_PA3
0xfd0d:   [None     ,   'f'],   # 3270_Test
0xfd0e:   [None     ,   'f'],   # 3270_Attn
0xfd0f:   [None     ,   'f'],   # 3270_CursorBlink
0xfd10:   [None     ,   'f'],   # 3270_AltCursor
0xfd11:   [None     ,   'f'],   # 3270_KeyClick
0xfd12:   [None     ,   'f'],   # 3270_Jump
0xfd13:   [None     ,   'f'],   # 3270_Ident
0xfd14:   [None     ,   'f'],   # 3270_Rule
0xfd15:   [None     ,   'f'],   # 3270_Copy
0xfd16:   [None     ,   'f'],   # 3270_Play
0xfd17:   [None     ,   'f'],   # 3270_Setup
0xfd18:   [None     ,   'f'],   # 3270_Record
0xfd19:   [None     ,   'f'],   # 3270_ChangeScreen
0xfd1a:   [None     ,   'f'],   # 3270_DeleteWord
0xfd1b:   [None     ,   'f'],   # 3270_ExSelect
0xfd1c:   [None     ,   'f'],   # 3270_CursorSelect
0xfd1d:   [None     ,   'f'],   # 3270_PrintScreen
0xfd1e:   [None     ,   'f'],   # 3270_Enter
0xfe01:   [None     ,   'f'],   # ISO_Lock
0xfe02:   [None     ,   'f'],   # ISO_Level2_Latch
0xfe03:   [None     ,   'f'],   # ISO_Level3_Shift
0xfe04:   [None     ,   'f'],   # ISO_Level3_Latch
0xfe05:   [None     ,   'f'],   # ISO_Level3_Lock
0xfe06:   [None     ,   'f'],   # ISO_Group_Latch
0xfe07:   [None     ,   'f'],   # ISO_Group_Lock
0xfe08:   [None     ,   'f'],   # ISO_Next_Group
0xfe09:   [None     ,   'f'],   # ISO_Next_Group_Lock
0xfe0a:   [None     ,   'f'],   # ISO_Prev_Group
0xfe0b:   [None     ,   'f'],   # ISO_Prev_Group_Lock
0xfe0c:   [None     ,   'f'],   # ISO_First_Group
0xfe0d:   [None     ,   'f'],   # ISO_First_Group_Lock
0xfe0e:   [None     ,   'f'],   # ISO_Last_Group
0xfe0f:   [None     ,   'f'],   # ISO_Last_Group_Lock
0xfe20:   [None     ,   'f'],   # ISO_Left_Tab
0xfe21:   [None     ,   'f'],   # ISO_Move_Line_Up
0xfe22:   [None     ,   'f'],   # ISO_Move_Line_Down
0xfe23:   [None     ,   'f'],   # ISO_Partial_Line_Up
0xfe24:   [None     ,   'f'],   # ISO_Partial_Line_Down
0xfe25:   [None     ,   'f'],   # ISO_Partial_Space_Left
0xfe26:   [None     ,   'f'],   # ISO_Partial_Space_Right
0xfe27:   [None     ,   'f'],   # ISO_Set_Margin_Left
0xfe28:   [None     ,   'f'],   # ISO_Set_Margin_Right
0xfe29:   [None     ,   'f'],   # ISO_Release_Margin_Left
0xfe2a:   [None     ,   'f'],   # ISO_Release_Margin_Right
0xfe2b:   [None     ,   'f'],   # ISO_Release_Both_Margins
0xfe2c:   [None     ,   'f'],   # ISO_Fast_Cursor_Left
0xfe2d:   [None     ,   'f'],   # ISO_Fast_Cursor_Right
0xfe2e:   [None     ,   'f'],   # ISO_Fast_Cursor_Up
0xfe2f:   [None     ,   'f'],   # ISO_Fast_Cursor_Down
0xfe30:   [None     ,   'f'],   # ISO_Continuous_Underline
0xfe31:   [None     ,   'f'],   # ISO_Discontinuous_Underline
0xfe32:   [None     ,   'f'],   # ISO_Emphasize
0xfe33:   [None     ,   'f'],   # ISO_Center_Object
0xfe34:   [None     ,   'f'],   # ISO_Enter
0xfe50:   [u'\u0300',   'f'],   # dead_grave
0xfe51:   [u'\u0301',   'f'],   # dead_acute
0xfe52:   [u'\u0302',   'f'],   # dead_circumflex
0xfe53:   [u'\u0303',   'f'],   # dead_tilde
0xfe54:   [u'\u0304',   'f'],   # dead_macron
0xfe55:   [u'\u0306',   'f'],   # dead_breve
0xfe56:   [u'\u0307',   'f'],   # dead_abovedot
0xfe57:   [u'\u0308',   'f'],   # dead_diaeresis
0xfe58:   [u'\u030a',   'f'],   # dead_abovering
0xfe59:   [u'\u030b',   'f'],   # dead_doubleacute
0xfe5a:   [u'\u030c',   'f'],   # dead_caron
0xfe5b:   [u'\u0327',   'f'],   # dead_cedilla
0xfe5c:   [u'\u0328',   'f'],   # dead_ogonek
0xfe5d:   [u'\u0345',   'f'],   # dead_iota
0xfe5e:   [u'\u3099',   'f'],   # dead_voiced_sound
0xfe5f:   [u'\u309a',   'f'],   # dead_semivoiced_sound
0xfe70:   [None     ,   'f'],   # AccessX_Enable
0xfe71:   [None     ,   'f'],   # AccessX_Feedback_Enable
0xfe72:   [None     ,   'f'],   # RepeatKeys_Enable
0xfe73:   [None     ,   'f'],   # SlowKeys_Enable
0xfe74:   [None     ,   'f'],   # BounceKeys_Enable
0xfe75:   [None     ,   'f'],   # StickyKeys_Enable
0xfe76:   [None     ,   'f'],   # MouseKeys_Enable
0xfe77:   [None     ,   'f'],   # MouseKeys_Accel_Enable
0xfe78:   [None     ,   'f'],   # Overlay1_Enable
0xfe79:   [None     ,   'f'],   # Overlay2_Enable
0xfe7a:   [None     ,   'f'],   # AudibleBell_Enable
0xfed0:   [None     ,   'f'],   # First_Virtual_Screen
0xfed1:   [None     ,   'f'],   # Prev_Virtual_Screen
0xfed2:   [None     ,   'f'],   # Next_Virtual_Screen
0xfed4:   [None     ,   'f'],   # Last_Virtual_Screen
0xfed5:   [None     ,   'f'],   # Terminate_Server
0xfee0:   [None     ,   'f'],   # Pointer_Left
0xfee1:   [None     ,   'f'],   # Pointer_Right
0xfee2:   [None     ,   'f'],   # Pointer_Up
0xfee3:   [None     ,   'f'],   # Pointer_Down
0xfee4:   [None     ,   'f'],   # Pointer_UpLeft
0xfee5:   [None     ,   'f'],   # Pointer_UpRight
0xfee6:   [None     ,   'f'],   # Pointer_DownLeft
0xfee7:   [None     ,   'f'],   # Pointer_DownRight
0xfee8:   [None     ,   'f'],   # Pointer_Button_Dflt
0xfee9:   [None     ,   'f'],   # Pointer_Button1
0xfeea:   [None     ,   'f'],   # Pointer_Button2
0xfeeb:   [None     ,   'f'],   # Pointer_Button3
0xfeec:   [None     ,   'f'],   # Pointer_Button4
0xfeed:   [None     ,   'f'],   # Pointer_Button5
0xfeee:   [None     ,   'f'],   # Pointer_DblClick_Dflt
0xfeef:   [None     ,   'f'],   # Pointer_DblClick1
0xfef0:   [None     ,   'f'],   # Pointer_DblClick2
0xfef1:   [None     ,   'f'],   # Pointer_DblClick3
0xfef2:   [None     ,   'f'],   # Pointer_DblClick4
0xfef3:   [None     ,   'f'],   # Pointer_DblClick5
0xfef4:   [None     ,   'f'],   # Pointer_Drag_Dflt
0xfef5:   [None     ,   'f'],   # Pointer_Drag1
0xfef6:   [None     ,   'f'],   # Pointer_Drag2
0xfef7:   [None     ,   'f'],   # Pointer_Drag3
0xfef8:   [None     ,   'f'],   # Pointer_Drag4
0xfef9:   [None     ,   'f'],   # Pointer_EnableKeys
0xfefa:   [None     ,   'f'],   # Pointer_Accelerate
0xfefb:   [None     ,   'f'],   # Pointer_DfltBtnNext
0xfefc:   [None     ,   'f'],   # Pointer_DfltBtnPrev
0xfefd:   [None     ,   'f'],   # Pointer_Drag5
0xff08:   [u'\u0008',   'f'],   # BackSpace	/* back space, back char */
0xff09:   [u'\u0009',   'f'],   # Tab
0xff0a:   [u'\u000a',   'f'],   # Linefeed	/* Linefeed, LF */
0xff0b:   [u'\u000b',   'f'],   # Clear
0xff0d:   [u'\u000d',   'f'],   # Return	/* Return, enter */
0xff13:   [u'\u0013',   'f'],   # Pause	/* Pause, hold */
0xff14:   [u'\u0014',   'f'],   # Scroll_Lock
0xff15:   [u'\u0015',   'f'],   # Sys_Req
0xff1b:   [u'\u001b',   'f'],   # Escape
0xff20:   [None     ,   'f'],   # Multi_key
0xff21:   [None     ,   'f'],   # Kanji
0xff22:   [None     ,   'f'],   # Muhenkan
0xff23:   [None     ,   'f'],   # Henkan_Mode
0xff24:   [None     ,   'f'],   # Romaji
0xff25:   [None     ,   'f'],   # Hiragana
0xff26:   [None     ,   'f'],   # Katakana
0xff27:   [None     ,   'f'],   # Hiragana_Katakana
0xff28:   [None     ,   'f'],   # Zenkaku
0xff29:   [None     ,   'f'],   # Hankaku
0xff2a:   [None     ,   'f'],   # Zenkaku_Hankaku
0xff2b:   [None     ,   'f'],   # Touroku
0xff2c:   [None     ,   'f'],   # Massyo
0xff2d:   [None     ,   'f'],   # Kana_Lock
0xff2e:   [None     ,   'f'],   # Kana_Shift
0xff2f:   [None     ,   'f'],   # Eisu_Shift
0xff30:   [None     ,   'f'],   # Eisu_toggle
0xff31:   [None     ,   'f'],   # Hangul
0xff32:   [None     ,   'f'],   # Hangul_Start
0xff33:   [None     ,   'f'],   # Hangul_End
0xff34:   [None     ,   'f'],   # Hangul_Hanja
0xff35:   [None     ,   'f'],   # Hangul_Jamo
0xff36:   [None     ,   'f'],   # Hangul_Romaja
0xff37:   [None     ,   'f'],   # Codeinput
0xff38:   [None     ,   'f'],   # Hangul_Jeonja
0xff39:   [None     ,   'f'],   # Hangul_Banja
0xff3a:   [None     ,   'f'],   # Hangul_PreHanja
0xff3b:   [None     ,   'f'],   # Hangul_PostHanja
0xff3c:   [None     ,   'f'],   # SingleCandidate
0xff3d:   [None     ,   'f'],   # MultipleCandidate
0xff3e:   [None     ,   'f'],   # PreviousCandidate
0xff3f:   [None     ,   'f'],   # Hangul_Special
0xff50:   [None     ,   'f'],   # Home
0xff51:   [None     ,   'f'],   # Left
0xff52:   [None     ,   'f'],   # Up
0xff53:   [None     ,   'f'],   # Right
0xff54:   [None     ,   'f'],   # Down
0xff55:   [None     ,   'f'],   # Prior
0xff56:   [None     ,   'f'],   # Next
0xff57:   [None     ,   'f'],   # End
0xff58:   [None     ,   'f'],   # Begin
0xff60:   [None     ,   'f'],   # Select
0xff61:   [None     ,   'f'],   # Print
0xff62:   [None     ,   'f'],   # Execute
0xff63:   [None     ,   'f'],   # Insert
0xff65:   [None     ,   'f'],   # Undo
0xff66:   [None     ,   'f'],   # Redo
0xff67:   [None     ,   'f'],   # Menu
0xff68:   [None     ,   'f'],   # Find
0xff69:   [None     ,   'f'],   # Cancel
0xff6a:   [None     ,   'f'],   # Help
0xff6b:   [None     ,   'f'],   # Break
0xff7e:   [None     ,   'f'],   # Mode_switch
0xff7f:   [None     ,   'f'],   # Num_Lock
0xff80:   [u'\u0020',   'f'],   # KP_Space	/* space */
0xff89:   [u'\u0009',   'f'],   # KP_Tab
0xff8d:   [u'\u000d',   'f'],   # KP_Enter	/* enter */
0xff91:   [None     ,   'f'],   # KP_F1
0xff92:   [None     ,   'f'],   # KP_F2
0xff93:   [None     ,   'f'],   # KP_F3
0xff94:   [None     ,   'f'],   # KP_F4
0xff95:   [None     ,   'f'],   # KP_Home
0xff96:   [None     ,   'f'],   # KP_Left
0xff97:   [None     ,   'f'],   # KP_Up
0xff98:   [None     ,   'f'],   # KP_Right
0xff99:   [None     ,   'f'],   # KP_Down
0xff9a:   [None     ,   'f'],   # KP_Prior
0xff9b:   [None     ,   'f'],   # KP_Next
0xff9c:   [None     ,   'f'],   # KP_End
0xff9d:   [None     ,   'f'],   # KP_Begin
0xff9e:   [None     ,   'f'],   # KP_Insert
0xff9f:   [None     ,   'f'],   # KP_Delete
0xffaa:   [u'\u002a',   'f'],   # KP_Multiply
0xffab:   [u'\u002b',   'f'],   # KP_Add
0xffac:   [u'\u002c',   'f'],   # KP_Separator	/* separator, often comma */
0xffad:   [u'\u002d',   'f'],   # KP_Subtract
0xffae:   [u'\u002e',   'f'],   # KP_Decimal
0xffaf:   [u'\u002f',   'f'],   # KP_Divide
0xffb0:   [u'\u0030',   'f'],   # KP_0
0xffb1:   [u'\u0031',   'f'],   # KP_1
0xffb2:   [u'\u0032',   'f'],   # KP_2
0xffb3:   [u'\u0033',   'f'],   # KP_3
0xffb4:   [u'\u0034',   'f'],   # KP_4
0xffb5:   [u'\u0035',   'f'],   # KP_5
0xffb6:   [u'\u0036',   'f'],   # KP_6
0xffb7:   [u'\u0037',   'f'],   # KP_7
0xffb8:   [u'\u0038',   'f'],   # KP_8
0xffb9:   [u'\u0039',   'f'],   # KP_9
0xffbd:   [u'\u003d',   'f'],   # KP_Equal	/* equals */
0xffbe:   [None     ,   'f'],   # F1
0xffbf:   [None     ,   'f'],   # F2
0xffc0:   [None     ,   'f'],   # F3
0xffc1:   [None     ,   'f'],   # F4
0xffc2:   [None     ,   'f'],   # F5
0xffc3:   [None     ,   'f'],   # F6
0xffc4:   [None     ,   'f'],   # F7
0xffc5:   [None     ,   'f'],   # F8
0xffc6:   [None     ,   'f'],   # F9
0xffc7:   [None     ,   'f'],   # F10
0xffc8:   [None     ,   'f'],   # F11
0xffc9:   [None     ,   'f'],   # F12
0xffca:   [None     ,   'f'],   # F13
0xffcb:   [None     ,   'f'],   # F14
0xffcc:   [None     ,   'f'],   # F15
0xffcd:   [None     ,   'f'],   # F16
0xffce:   [None     ,   'f'],   # F17
0xffcf:   [None     ,   'f'],   # F18
0xffd0:   [None     ,   'f'],   # F19
0xffd1:   [None     ,   'f'],   # F20
0xffd2:   [None     ,   'f'],   # F21
0xffd3:   [None     ,   'f'],   # F22
0xffd4:   [None     ,   'f'],   # F23
0xffd5:   [None     ,   'f'],   # F24
0xffd6:   [None     ,   'f'],   # F25
0xffd7:   [None     ,   'f'],   # F26
0xffd8:   [None     ,   'f'],   # F27
0xffd9:   [None     ,   'f'],   # F28
0xffda:   [None     ,   'f'],   # F29
0xffdb:   [None     ,   'f'],   # F30
0xffdc:   [None     ,   'f'],   # F31
0xffdd:   [None     ,   'f'],   # F32
0xffde:   [None     ,   'f'],   # F33
0xffdf:   [None     ,   'f'],   # F34
0xffe0:   [None     ,   'f'],   # F35
0xffe1:   [None     ,   'f'],   # Shift_L
0xffe2:   [None     ,   'f'],   # Shift_R
0xffe3:   [None     ,   'f'],   # Control_L
0xffe4:   [None     ,   'f'],   # Control_R
0xffe5:   [None     ,   'f'],   # Caps_Lock
0xffe6:   [None     ,   'f'],   # Shift_Lock
0xffe7:   [None     ,   'f'],   # Meta_L
0xffe8:   [None     ,   'f'],   # Meta_R
0xffe9:   [None     ,   'f'],   # Alt_L
0xffea:   [None     ,   'f'],   # Alt_R
0xffeb:   [None     ,   'f'],   # Super_L
0xffec:   [None     ,   'f'],   # Super_R
0xffed:   [None     ,   'f'],   # Hyper_L
0xffee:   [None     ,   'f'],   # Hyper_R
0xffff:   [None     ,   'f'],   # Delete
0xffffff: [None     ,   'f'],   # VoidSymbol

# Various XFree86 extensions since X11R6.4
# http://cvsweb.xfree86.org/cvsweb/xc/include/keysymdef.h

# KOI8-U support (Aleksey Novodvorsky, 1999-05-30)
# http://cvsweb.xfree86.org/cvsweb/xc/include/keysymdef.h.diff?r1=1.4&r2=1.5
# Used in XFree86's /usr/lib/X11/xkb/symbols/ua mappings

0x06ad:   [u'\u0491',   '.'],   # Ukrainian_ghe_with_upturn
0x06bd:   [u'\u0490',   '.'],   # Ukrainian_GHE_WITH_UPTURN

# Support for armscii-8, ibm-cp1133, mulelao-1, viscii1.1-1,
# tcvn-5712, georgian-academy, georgian-ps
# (#2843, Pablo Saratxaga <pablo@mandrakesoft.com>, 1999-06-06)
# http://cvsweb.xfree86.org/cvsweb/xc/include/keysymdef.h.diff?r1=1.6&r2=1.7

# Armenian
# (not used in any XFree86 4.4 kbd layouts, where /usr/lib/X11/xkb/symbols/am
# uses directly Unicode-mapped hexadecimal values instead)
0x14a1:   [None     ,   'r'],   # Armenian_eternity
0x14a2:   [u'\u0587',   'u'],   # Armenian_ligature_ew
0x14a3:   [u'\u0589',   'u'],   # Armenian_verjaket
0x14a4:   [u'\u0029',   'r'],   # Armenian_parenright
0x14a5:   [u'\u0028',   'r'],   # Armenian_parenleft
0x14a6:   [u'\u00bb',   'r'],   # Armenian_guillemotright
0x14a7:   [u'\u00ab',   'r'],   # Armenian_guillemotleft
0x14a8:   [u'\u2014',   'r'],   # Armenian_em_dash
0x14a9:   [u'\u002e',   'r'],   # Armenian_mijaket
0x14aa:   [u'\u055d',   'u'],   # Armenian_but
0x14ab:   [u'\u002c',   'r'],   # Armenian_comma
0x14ac:   [u'\u2013',   'r'],   # Armenian_en_dash
0x14ad:   [u'\u058a',   'u'],   # Armenian_yentamna
0x14ae:   [u'\u2026',   'r'],   # Armenian_ellipsis
0x14af:   [u'\u055c',   'u'],   # Armenian_amanak
0x14b0:   [u'\u055b',   'u'],   # Armenian_shesht
0x14b1:   [u'\u055e',   'u'],   # Armenian_paruyk
0x14b2:   [u'\u0531',   'u'],   # Armenian_AYB
0x14b3:   [u'\u0561',   'u'],   # Armenian_ayb
0x14b4:   [u'\u0532',   'u'],   # Armenian_BEN
0x14b5:   [u'\u0562',   'u'],   # Armenian_ben
0x14b6:   [u'\u0533',   'u'],   # Armenian_GIM
0x14b7:   [u'\u0563',   'u'],   # Armenian_gim
0x14b8:   [u'\u0534',   'u'],   # Armenian_DA
0x14b9:   [u'\u0564',   'u'],   # Armenian_da
0x14ba:   [u'\u0535',   'u'],   # Armenian_YECH
0x14bb:   [u'\u0565',   'u'],   # Armenian_yech
0x14bc:   [u'\u0536',   'u'],   # Armenian_ZA
0x14bd:   [u'\u0566',   'u'],   # Armenian_za
0x14be:   [u'\u0537',   'u'],   # Armenian_E
0x14bf:   [u'\u0567',   'u'],   # Armenian_e
0x14c0:   [u'\u0538',   'u'],   # Armenian_AT
0x14c1:   [u'\u0568',   'u'],   # Armenian_at
0x14c2:   [u'\u0539',   'u'],   # Armenian_TO
0x14c3:   [u'\u0569',   'u'],   # Armenian_to
0x14c4:   [u'\u053a',   'u'],   # Armenian_ZHE
0x14c5:   [u'\u056a',   'u'],   # Armenian_zhe
0x14c6:   [u'\u053b',   'u'],   # Armenian_INI
0x14c7:   [u'\u056b',   'u'],   # Armenian_ini
0x14c8:   [u'\u053c',   'u'],   # Armenian_LYUN
0x14c9:   [u'\u056c',   'u'],   # Armenian_lyun
0x14ca:   [u'\u053d',   'u'],   # Armenian_KHE
0x14cb:   [u'\u056d',   'u'],   # Armenian_khe
0x14cc:   [u'\u053e',   'u'],   # Armenian_TSA
0x14cd:   [u'\u056e',   'u'],   # Armenian_tsa
0x14ce:   [u'\u053f',   'u'],   # Armenian_KEN
0x14cf:   [u'\u056f',   'u'],   # Armenian_ken
0x14d0:   [u'\u0540',   'u'],   # Armenian_HO
0x14d1:   [u'\u0570',   'u'],   # Armenian_ho
0x14d2:   [u'\u0541',   'u'],   # Armenian_DZA
0x14d3:   [u'\u0571',   'u'],   # Armenian_dza
0x14d4:   [u'\u0542',   'u'],   # Armenian_GHAT
0x14d5:   [u'\u0572',   'u'],   # Armenian_ghat
0x14d6:   [u'\u0543',   'u'],   # Armenian_TCHE
0x14d7:   [u'\u0573',   'u'],   # Armenian_tche
0x14d8:   [u'\u0544',   'u'],   # Armenian_MEN
0x14d9:   [u'\u0574',   'u'],   # Armenian_men
0x14da:   [u'\u0545',   'u'],   # Armenian_HI
0x14db:   [u'\u0575',   'u'],   # Armenian_hi
0x14dc:   [u'\u0546',   'u'],   # Armenian_NU
0x14dd:   [u'\u0576',   'u'],   # Armenian_nu
0x14de:   [u'\u0547',   'u'],   # Armenian_SHA
0x14df:   [u'\u0577',   'u'],   # Armenian_sha
0x14e0:   [u'\u0548',   'u'],   # Armenian_VO
0x14e1:   [u'\u0578',   'u'],   # Armenian_vo
0x14e2:   [u'\u0549',   'u'],   # Armenian_CHA
0x14e3:   [u'\u0579',   'u'],   # Armenian_cha
0x14e4:   [u'\u054a',   'u'],   # Armenian_PE
0x14e5:   [u'\u057a',   'u'],   # Armenian_pe
0x14e6:   [u'\u054b',   'u'],   # Armenian_JE
0x14e7:   [u'\u057b',   'u'],   # Armenian_je
0x14e8:   [u'\u054c',   'u'],   # Armenian_RA
0x14e9:   [u'\u057c',   'u'],   # Armenian_ra
0x14ea:   [u'\u054d',   'u'],   # Armenian_SE
0x14eb:   [u'\u057d',   'u'],   # Armenian_se
0x14ec:   [u'\u054e',   'u'],   # Armenian_VEV
0x14ed:   [u'\u057e',   'u'],   # Armenian_vev
0x14ee:   [u'\u054f',   'u'],   # Armenian_TYUN
0x14ef:   [u'\u057f',   'u'],   # Armenian_tyun
0x14f0:   [u'\u0550',   'u'],   # Armenian_RE
0x14f1:   [u'\u0580',   'u'],   # Armenian_re
0x14f2:   [u'\u0551',   'u'],   # Armenian_TSO
0x14f3:   [u'\u0581',   'u'],   # Armenian_tso
0x14f4:   [u'\u0552',   'u'],   # Armenian_VYUN
0x14f5:   [u'\u0582',   'u'],   # Armenian_vyun
0x14f6:   [u'\u0553',   'u'],   # Armenian_PYUR
0x14f7:   [u'\u0583',   'u'],   # Armenian_pyur
0x14f8:   [u'\u0554',   'u'],   # Armenian_KE
0x14f9:   [u'\u0584',   'u'],   # Armenian_ke
0x14fa:   [u'\u0555',   'u'],   # Armenian_O
0x14fb:   [u'\u0585',   'u'],   # Armenian_o
0x14fc:   [u'\u0556',   'u'],   # Armenian_FE
0x14fd:   [u'\u0586',   'u'],   # Armenian_fe
0x14fe:   [u'\u055a',   'u'],   # Armenian_apostrophe
0x14ff:   [u'\u00a7',   'r'],   # Armenian_section_sign

# Gregorian
# (not used in any XFree86 4.4 kbd layouts, were /usr/lib/X11/xkb/symbols/ge_*
# uses directly Unicode-mapped hexadecimal values instead)
0x15d0:   [u'\u10d0',   'u'],   # Georgian_an
0x15d1:   [u'\u10d1',   'u'],   # Georgian_ban
0x15d2:   [u'\u10d2',   'u'],   # Georgian_gan
0x15d3:   [u'\u10d3',   'u'],   # Georgian_don
0x15d4:   [u'\u10d4',   'u'],   # Georgian_en
0x15d5:   [u'\u10d5',   'u'],   # Georgian_vin
0x15d6:   [u'\u10d6',   'u'],   # Georgian_zen
0x15d7:   [u'\u10d7',   'u'],   # Georgian_tan
0x15d8:   [u'\u10d8',   'u'],   # Georgian_in
0x15d9:   [u'\u10d9',   'u'],   # Georgian_kan
0x15da:   [u'\u10da',   'u'],   # Georgian_las
0x15db:   [u'\u10db',   'u'],   # Georgian_man
0x15dc:   [u'\u10dc',   'u'],   # Georgian_nar
0x15dd:   [u'\u10dd',   'u'],   # Georgian_on
0x15de:   [u'\u10de',   'u'],   # Georgian_par
0x15df:   [u'\u10df',   'u'],   # Georgian_zhar
0x15e0:   [u'\u10e0',   'u'],   # Georgian_rae
0x15e1:   [u'\u10e1',   'u'],   # Georgian_san
0x15e2:   [u'\u10e2',   'u'],   # Georgian_tar
0x15e3:   [u'\u10e3',   'u'],   # Georgian_un
0x15e4:   [u'\u10e4',   'u'],   # Georgian_phar
0x15e5:   [u'\u10e5',   'u'],   # Georgian_khar
0x15e6:   [u'\u10e6',   'u'],   # Georgian_ghan
0x15e7:   [u'\u10e7',   'u'],   # Georgian_qar
0x15e8:   [u'\u10e8',   'u'],   # Georgian_shin
0x15e9:   [u'\u10e9',   'u'],   # Georgian_chin
0x15ea:   [u'\u10ea',   'u'],   # Georgian_can
0x15eb:   [u'\u10eb',   'u'],   # Georgian_jil
0x15ec:   [u'\u10ec',   'u'],   # Georgian_cil
0x15ed:   [u'\u10ed',   'u'],   # Georgian_char
0x15ee:   [u'\u10ee',   'u'],   # Georgian_xan
0x15ef:   [u'\u10ef',   'u'],   # Georgian_jhan
0x15f0:   [u'\u10f0',   'u'],   # Georgian_hae
0x15f1:   [u'\u10f1',   'u'],   # Georgian_he
0x15f2:   [u'\u10f2',   'u'],   # Georgian_hie
0x15f3:   [u'\u10f3',   'u'],   # Georgian_we
0x15f4:   [u'\u10f4',   'u'],   # Georgian_har
0x15f5:   [u'\u10f5',   'u'],   # Georgian_hoe
0x15f6:   [u'\u10f6',   'u'],   # Georgian_fi

# Pablo Saratxaga's i18n updates for XFree86 that are used in Mandrake 7.2.
# (#4195, Pablo Saratxaga <pablo@mandrakesoft.com>, 2000-10-27)
# http://cvsweb.xfree86.org/cvsweb/xc/include/keysymdef.h.diff?r1=1.9&r2=1.10

# Latin-8
# (the *abovedot keysyms are used in /usr/lib/X11/xkb/symbols/ie)
0x12a1:   [u'\u1e02',   'u'],   # Babovedot
0x12a2:   [u'\u1e03',   'u'],   # babovedot
0x12a6:   [u'\u1e0a',   'u'],   # Dabovedot
0x12a8:   [u'\u1e80',   'u'],   # Wgrave
0x12aa:   [u'\u1e82',   'u'],   # Wacute
0x12ab:   [u'\u1e0b',   'u'],   # dabovedot
0x12ac:   [u'\u1ef2',   'u'],   # Ygrave
0x12b0:   [u'\u1e1e',   'u'],   # Fabovedot
0x12b1:   [u'\u1e1f',   'u'],   # fabovedot
0x12b4:   [u'\u1e40',   'u'],   # Mabovedot
0x12b5:   [u'\u1e41',   'u'],   # mabovedot
0x12b7:   [u'\u1e56',   'u'],   # Pabovedot
0x12b8:   [u'\u1e81',   'u'],   # wgrave
0x12b9:   [u'\u1e57',   'u'],   # pabovedot
0x12ba:   [u'\u1e83',   'u'],   # wacute
0x12bb:   [u'\u1e60',   'u'],   # Sabovedot
0x12bc:   [u'\u1ef3',   'u'],   # ygrave
0x12bd:   [u'\u1e84',   'u'],   # Wdiaeresis
0x12be:   [u'\u1e85',   'u'],   # wdiaeresis
0x12bf:   [u'\u1e61',   'u'],   # sabovedot
0x12d0:   [u'\u0174',   'u'],   # Wcircumflex
0x12d7:   [u'\u1e6a',   'u'],   # Tabovedot
0x12de:   [u'\u0176',   'u'],   # Ycircumflex
0x12f0:   [u'\u0175',   'u'],   # wcircumflex
0x12f7:   [u'\u1e6b',   'u'],   # tabovedot
0x12fe:   [u'\u0177',   'u'],   # ycircumflex

# Arabic
# (of these, in XFree86 4.4 only Arabic_superscript_alef, Arabic_madda_above,
# Arabic_hamza_* are actually used, e.g. in /usr/lib/X11/xkb/symbols/syr)
0x0590:   [u'\u06f0',   'u'],   # Farsi_0
0x0591:   [u'\u06f1',   'u'],   # Farsi_1
0x0592:   [u'\u06f2',   'u'],   # Farsi_2
0x0593:   [u'\u06f3',   'u'],   # Farsi_3
0x0594:   [u'\u06f4',   'u'],   # Farsi_4
0x0595:   [u'\u06f5',   'u'],   # Farsi_5
0x0596:   [u'\u06f6',   'u'],   # Farsi_6
0x0597:   [u'\u06f7',   'u'],   # Farsi_7
0x0598:   [u'\u06f8',   'u'],   # Farsi_8
0x0599:   [u'\u06f9',   'u'],   # Farsi_9
0x05a5:   [u'\u066a',   'u'],   # Arabic_percent
0x05a6:   [u'\u0670',   'u'],   # Arabic_superscript_alef
0x05a7:   [u'\u0679',   'u'],   # Arabic_tteh
0x05a8:   [u'\u067e',   'u'],   # Arabic_peh
0x05a9:   [u'\u0686',   'u'],   # Arabic_tcheh
0x05aa:   [u'\u0688',   'u'],   # Arabic_ddal
0x05ab:   [u'\u0691',   'u'],   # Arabic_rreh
0x05ae:   [u'\u06d4',   'u'],   # Arabic_fullstop
0x05b0:   [u'\u0660',   'u'],   # Arabic_0
0x05b1:   [u'\u0661',   'u'],   # Arabic_1
0x05b2:   [u'\u0662',   'u'],   # Arabic_2
0x05b3:   [u'\u0663',   'u'],   # Arabic_3
0x05b4:   [u'\u0664',   'u'],   # Arabic_4
0x05b5:   [u'\u0665',   'u'],   # Arabic_5
0x05b6:   [u'\u0666',   'u'],   # Arabic_6
0x05b7:   [u'\u0667',   'u'],   # Arabic_7
0x05b8:   [u'\u0668',   'u'],   # Arabic_8
0x05b9:   [u'\u0669',   'u'],   # Arabic_9
0x05f3:   [u'\u0653',   'u'],   # Arabic_madda_above
0x05f4:   [u'\u0654',   'u'],   # Arabic_hamza_above
0x05f5:   [u'\u0655',   'u'],   # Arabic_hamza_below
0x05f6:   [u'\u0698',   'u'],   # Arabic_jeh
0x05f7:   [u'\u06a4',   'u'],   # Arabic_veh
0x05f8:   [u'\u06a9',   'u'],   # Arabic_keheh
0x05f9:   [u'\u06af',   'u'],   # Arabic_gaf
0x05fa:   [u'\u06ba',   'u'],   # Arabic_noon_ghunna
0x05fb:   [u'\u06be',   'u'],   # Arabic_heh_doachashmee
0x05fc:   [u'\u06cc',   'u'],   # Farsi_yeh
0x05fd:   [u'\u06d2',   'u'],   # Arabic_yeh_baree
0x05fe:   [u'\u06c1',   'u'],   # Arabic_heh_goal

# Cyrillic
# (none of these are actually used in any XFree86 4.4 kbd layouts)
0x0680:   [u'\u0492',   'u'],   # Cyrillic_GHE_bar
0x0681:   [u'\u0496',   'u'],   # Cyrillic_ZHE_descender
0x0682:   [u'\u049a',   'u'],   # Cyrillic_KA_descender
0x0683:   [u'\u049c',   'u'],   # Cyrillic_KA_vertstroke
0x0684:   [u'\u04a2',   'u'],   # Cyrillic_EN_descender
0x0685:   [u'\u04ae',   'u'],   # Cyrillic_U_straight
0x0686:   [u'\u04b0',   'u'],   # Cyrillic_U_straight_bar
0x0687:   [u'\u04b2',   'u'],   # Cyrillic_HA_descender
0x0688:   [u'\u04b6',   'u'],   # Cyrillic_CHE_descender
0x0689:   [u'\u04b8',   'u'],   # Cyrillic_CHE_vertstroke
0x068a:   [u'\u04ba',   'u'],   # Cyrillic_SHHA
0x068c:   [u'\u04d8',   'u'],   # Cyrillic_SCHWA
0x068d:   [u'\u04e2',   'u'],   # Cyrillic_I_macron
0x068e:   [u'\u04e8',   'u'],   # Cyrillic_O_bar
0x068f:   [u'\u04ee',   'u'],   # Cyrillic_U_macron
0x0690:   [u'\u0493',   'u'],   # Cyrillic_ghe_bar
0x0691:   [u'\u0497',   'u'],   # Cyrillic_zhe_descender
0x0692:   [u'\u049b',   'u'],   # Cyrillic_ka_descender
0x0693:   [u'\u049d',   'u'],   # Cyrillic_ka_vertstroke
0x0694:   [u'\u04a3',   'u'],   # Cyrillic_en_descender
0x0695:   [u'\u04af',   'u'],   # Cyrillic_u_straight
0x0696:   [u'\u04b1',   'u'],   # Cyrillic_u_straight_bar
0x0697:   [u'\u04b3',   'u'],   # Cyrillic_ha_descender
0x0698:   [u'\u04b7',   'u'],   # Cyrillic_che_descender
0x0699:   [u'\u04b9',   'u'],   # Cyrillic_che_vertstroke
0x069a:   [u'\u04bb',   'u'],   # Cyrillic_shha
0x069c:   [u'\u04d9',   'u'],   # Cyrillic_schwa
0x069d:   [u'\u04e3',   'u'],   # Cyrillic_i_macron
0x069e:   [u'\u04e9',   'u'],   # Cyrillic_o_bar
0x069f:   [u'\u04ef',   'u'],   # Cyrillic_u_macron

# Caucasus
# (of these, in XFree86 4.4 only Gcaron, gcaron are actually used,
# e.g. in /usr/lib/X11/xkb/symbols/sapmi; the lack of Unicode
# equivalents for the others suggests that they are bogus)
0x16a2:   [None     ,   'r'],   # Ccedillaabovedot
0x16a3:   [u'\u1e8a',   'u'],   # Xabovedot
0x16a5:   [None     ,   'r'],   # Qabovedot
0x16a6:   [u'\u012c',   'u'],   # Ibreve
0x16a7:   [None     ,   'r'],   # IE
0x16a8:   [None     ,   'r'],   # UO
0x16a9:   [u'\u01b5',   'u'],   # Zstroke
0x16aa:   [u'\u01e6',   'u'],   # Gcaron
0x16af:   [u'\u019f',   'u'],   # Obarred
0x16b2:   [None     ,   'r'],   # ccedillaabovedot
0x16b3:   [u'\u1e8b',   'u'],   # xabovedot
0x16b4:   [None     ,   'r'],   # Ocaron
0x16b5:   [None     ,   'r'],   # qabovedot
0x16b6:   [u'\u012d',   'u'],   # ibreve
0x16b7:   [None     ,   'r'],   # ie
0x16b8:   [None     ,   'r'],   # uo
0x16b9:   [u'\u01b6',   'u'],   # zstroke
0x16ba:   [u'\u01e7',   'u'],   # gcaron
0x16bd:   [u'\u01d2',   'u'],   # ocaron
0x16bf:   [u'\u0275',   'u'],   # obarred
0x16c6:   [u'\u018f',   'u'],   # SCHWA
0x16f6:   [u'\u0259',   'u'],   # schwa

# Inupiak, Guarani
# (none of these are actually used in any XFree86 4.4 kbd layouts,
# and the lack of Unicode equivalents suggests that they are bogus)
0x16d1:   [u'\u1e36',   'u'],   # Lbelowdot
0x16d2:   [None     ,   'r'],   # Lstrokebelowdot
0x16d3:   [None     ,   'r'],   # Gtilde
0x16e1:   [u'\u1e37',   'u'],   # lbelowdot
0x16e2:   [None     ,   'r'],   # lstrokebelowdot
0x16e3:   [None     ,   'r'],   # gtilde

# Vietnamese
# (none of these are actually used in any XFree86 4.4 kbd layouts; they are
# also pointless, as Vietnamese input methods use dead accent keys + ASCII keys)
0x1ea0:   [u'\u1ea0',   'u'],   # Abelowdot
0x1ea1:   [u'\u1ea1',   'u'],   # abelowdot
0x1ea2:   [u'\u1ea2',   'u'],   # Ahook
0x1ea3:   [u'\u1ea3',   'u'],   # ahook
0x1ea4:   [u'\u1ea4',   'u'],   # Acircumflexacute
0x1ea5:   [u'\u1ea5',   'u'],   # acircumflexacute
0x1ea6:   [u'\u1ea6',   'u'],   # Acircumflexgrave
0x1ea7:   [u'\u1ea7',   'u'],   # acircumflexgrave
0x1ea8:   [u'\u1ea8',   'u'],   # Acircumflexhook
0x1ea9:   [u'\u1ea9',   'u'],   # acircumflexhook
0x1eaa:   [u'\u1eaa',   'u'],   # Acircumflextilde
0x1eab:   [u'\u1eab',   'u'],   # acircumflextilde
0x1eac:   [u'\u1eac',   'u'],   # Acircumflexbelowdot
0x1ead:   [u'\u1ead',   'u'],   # acircumflexbelowdot
0x1eae:   [u'\u1eae',   'u'],   # Abreveacute
0x1eaf:   [u'\u1eaf',   'u'],   # abreveacute
0x1eb0:   [u'\u1eb0',   'u'],   # Abrevegrave
0x1eb1:   [u'\u1eb1',   'u'],   # abrevegrave
0x1eb2:   [u'\u1eb2',   'u'],   # Abrevehook
0x1eb3:   [u'\u1eb3',   'u'],   # abrevehook
0x1eb4:   [u'\u1eb4',   'u'],   # Abrevetilde
0x1eb5:   [u'\u1eb5',   'u'],   # abrevetilde
0x1eb6:   [u'\u1eb6',   'u'],   # Abrevebelowdot
0x1eb7:   [u'\u1eb7',   'u'],   # abrevebelowdot
0x1eb8:   [u'\u1eb8',   'u'],   # Ebelowdot
0x1eb9:   [u'\u1eb9',   'u'],   # ebelowdot
0x1eba:   [u'\u1eba',   'u'],   # Ehook
0x1ebb:   [u'\u1ebb',   'u'],   # ehook
0x1ebc:   [u'\u1ebc',   'u'],   # Etilde
0x1ebd:   [u'\u1ebd',   'u'],   # etilde
0x1ebe:   [u'\u1ebe',   'u'],   # Ecircumflexacute
0x1ebf:   [u'\u1ebf',   'u'],   # ecircumflexacute
0x1ec0:   [u'\u1ec0',   'u'],   # Ecircumflexgrave
0x1ec1:   [u'\u1ec1',   'u'],   # ecircumflexgrave
0x1ec2:   [u'\u1ec2',   'u'],   # Ecircumflexhook
0x1ec3:   [u'\u1ec3',   'u'],   # ecircumflexhook
0x1ec4:   [u'\u1ec4',   'u'],   # Ecircumflextilde
0x1ec5:   [u'\u1ec5',   'u'],   # ecircumflextilde
0x1ec6:   [u'\u1ec6',   'u'],   # Ecircumflexbelowdot
0x1ec7:   [u'\u1ec7',   'u'],   # ecircumflexbelowdot
0x1ec8:   [u'\u1ec8',   'u'],   # Ihook
0x1ec9:   [u'\u1ec9',   'u'],   # ihook
0x1eca:   [u'\u1eca',   'u'],   # Ibelowdot
0x1ecb:   [u'\u1ecb',   'u'],   # ibelowdot
0x1ecc:   [u'\u1ecc',   'u'],   # Obelowdot
0x1ecd:   [u'\u1ecd',   'u'],   # obelowdot
0x1ece:   [u'\u1ece',   'u'],   # Ohook
0x1ecf:   [u'\u1ecf',   'u'],   # ohook
0x1ed0:   [u'\u1ed0',   'u'],   # Ocircumflexacute
0x1ed1:   [u'\u1ed1',   'u'],   # ocircumflexacute
0x1ed2:   [u'\u1ed2',   'u'],   # Ocircumflexgrave
0x1ed3:   [u'\u1ed3',   'u'],   # ocircumflexgrave
0x1ed4:   [u'\u1ed4',   'u'],   # Ocircumflexhook
0x1ed5:   [u'\u1ed5',   'u'],   # ocircumflexhook
0x1ed6:   [u'\u1ed6',   'u'],   # Ocircumflextilde
0x1ed7:   [u'\u1ed7',   'u'],   # ocircumflextilde
0x1ed8:   [u'\u1ed8',   'u'],   # Ocircumflexbelowdot
0x1ed9:   [u'\u1ed9',   'u'],   # ocircumflexbelowdot
0x1eda:   [u'\u1eda',   'u'],   # Ohornacute
0x1edb:   [u'\u1edb',   'u'],   # ohornacute
0x1edc:   [u'\u1edc',   'u'],   # Ohorngrave
0x1edd:   [u'\u1edd',   'u'],   # ohorngrave
0x1ede:   [u'\u1ede',   'u'],   # Ohornhook
0x1edf:   [u'\u1edf',   'u'],   # ohornhook
0x1ee0:   [u'\u1ee0',   'u'],   # Ohorntilde
0x1ee1:   [u'\u1ee1',   'u'],   # ohorntilde
0x1ee2:   [u'\u1ee2',   'u'],   # Ohornbelowdot
0x1ee3:   [u'\u1ee3',   'u'],   # ohornbelowdot
0x1ee4:   [u'\u1ee4',   'u'],   # Ubelowdot
0x1ee5:   [u'\u1ee5',   'u'],   # ubelowdot
0x1ee6:   [u'\u1ee6',   'u'],   # Uhook
0x1ee7:   [u'\u1ee7',   'u'],   # uhook
0x1ee8:   [u'\u1ee8',   'u'],   # Uhornacute
0x1ee9:   [u'\u1ee9',   'u'],   # uhornacute
0x1eea:   [u'\u1eea',   'u'],   # Uhorngrave
0x1eeb:   [u'\u1eeb',   'u'],   # uhorngrave
0x1eec:   [u'\u1eec',   'u'],   # Uhornhook
0x1eed:   [u'\u1eed',   'u'],   # uhornhook
0x1eee:   [u'\u1eee',   'u'],   # Uhorntilde
0x1eef:   [u'\u1eef',   'u'],   # uhorntilde
0x1ef0:   [u'\u1ef0',   'u'],   # Uhornbelowdot
0x1ef1:   [u'\u1ef1',   'u'],   # uhornbelowdot
0x1ef4:   [u'\u1ef4',   'u'],   # Ybelowdot
0x1ef5:   [u'\u1ef5',   'u'],   # ybelowdot
0x1ef6:   [u'\u1ef6',   'u'],   # Yhook
0x1ef7:   [u'\u1ef7',   'u'],   # yhook
0x1ef8:   [u'\u1ef8',   'u'],   # Ytilde
0x1ef9:   [u'\u1ef9',   'u'],   # ytilde

0x1efa:   [u'\u01a0',   'u'],   # Ohorn
0x1efb:   [u'\u01a1',   'u'],   # ohorn
0x1efc:   [u'\u01af',   'u'],   # Uhorn
0x1efd:   [u'\u01b0',   'u'],   # uhorn

# (Unicode combining characters have no direct equivalence with
# keysyms, where dead keys are defined instead)
0x1e9f:   [u'\u0303',   'r'],   # combining_tilde
0x1ef2:   [u'\u0300',   'r'],   # combining_grave
0x1ef3:   [u'\u0301',   'r'],   # combining_acute
0x1efe:   [u'\u0309',   'r'],   # combining_hook
0x1eff:   [u'\u0323',   'r'],   # combining_belowdot

# These probably should be added to the X11 standard properly,
# as they could be of use for Vietnamese input methods.
0xfe60:   [u'\u0323',   'f'],   # dead_belowdot
0xfe61:   [u'\u0309',   'f'],   # dead_hook
0xfe62:   [u'\u031b',   'f'],   # dead_horn

}
