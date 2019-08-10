" A vim global plugin to help with switching date formats.
" Maintainer: Shrikant Sharat Kandula
" License: MIT License

if exists('g:loaded_outdate')
  finish
endif
let g:loaded_outdate = 1

if !exists('g:outdate_parse_formats')
  let g:outdate_parse_formats = [
        \ '%d-%b-%Y',
        \ '%m/%d/%Y',
        \ '%Y-%m-%d',
        \ '%Y%m%d',
        \ ]
endif

command! -nargs=1 -range Outdate call <SID>Outdate(<f-args>, <line1>, <line2>, <range>)
fun! s:Outdate(...) abort
  py3 import vim, outdate
  py3 outdate.apply(*vim.eval('a:000'))
  silent! call repeat#set(":call Outdate('" . a:1 . "')\<CR>", v:count)
endfun

command! -nargs=+ OutdateMap call <SID>OutdateMap(<f-args>)
fun! s:OutdateMap(to_fmt, n_map, v_map) abort
  exe 'nnoremap ' . a:n_map . ' :Outdate ' . a:to_fmt . '<CR>'
  exe 'vnoremap ' . a:v_map . ' :Outdate ' . a:to_fmt . '<CR>'
endfun

if !get(g:, 'outdate_no_default_maps', 0)
  OutdateMap %d-%b-%Y cdo Do
  OutdateMap %m/%d/%Y cda Da
  OutdateMap %Y-%m-%d cdi Di
  OutdateMap %Y%m%d   cdn Dn
endif
