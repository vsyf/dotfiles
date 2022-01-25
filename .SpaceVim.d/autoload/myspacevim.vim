function! myspacevim#before() abort

" vim-template
let g:username='youfa.song'
let g:email='vsyfar@gmail.com'
let g:license='GPLv2'

  let g:coc_global_extensions = [
    \ 'coc-emoji',
    \ 'coc-json',
    \ 'coc-snippets',
    \ ]

endfunction



function! myspacevim#after() abort

inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"

endfunction
