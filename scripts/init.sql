CREATE TABLE `faucet` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`network` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`platform` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`address` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`status` INT(11) NULL DEFAULT NULL,
	`url` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`amount` BIGINT(20) NULL DEFAULT NULL,
	`transfered_txn` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`transfered_at` DATETIME NULL DEFAULT NULL,
	`created_at` DATETIME NULL DEFAULT NULL,
	`updated_at` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `ix_faucet_id` (`id`) USING BTREE,
	INDEX `ix_faucet_address` (`address`) USING BTREE,
	INDEX `ix_faucet_platform_transfered_at_status` (`platform`, `transfered_at`, `status`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
