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

fun! Outdate(to_fmt) abort
  py3 import vim, outdate
  py3 outdate.outdate_apply(vim.eval('a:to_fmt'))
  silent! call repeat#set(":call Outdate('" . a:to_fmt . "')\<CR>", v:count)
endfun

if !get(g:, 'outdate_no_default_maps', 0)
  nnoremap <silent> cdo :call Outdate('%d-%b-%Y')<CR>
  nnoremap <silent> cda :call Outdate('%m/%d/%Y')<CR>
  nnoremap <silent> cdi :call Outdate('%Y-%m-%d')<CR>
  nnoremap <silent> cdn :call Outdate('%Y%m%d')<CR>
endif
