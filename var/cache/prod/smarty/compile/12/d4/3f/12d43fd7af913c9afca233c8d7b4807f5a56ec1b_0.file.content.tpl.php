<?php
/* Smarty version 3.1.33, created on 2021-12-04 14:50:59
  from '/var/www/html/admin136kdo2mw/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.33',
  'unifunc' => 'content_61ab72435dfd94_96889558',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '12d43fd7af913c9afca233c8d7b4807f5a56ec1b' => 
    array (
      0 => '/var/www/html/admin136kdo2mw/themes/default/template/content.tpl',
      1 => 1638624713,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_61ab72435dfd94_96889558 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>


<div class="row">
	<div class="col-lg-12">
		<?php if (isset($_smarty_tpl->tpl_vars['content']->value)) {?>
			<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

		<?php }?>
	</div>
</div>
<?php }
}
