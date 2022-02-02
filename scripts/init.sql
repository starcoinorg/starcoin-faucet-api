DROP TABLE IF EXISTS `faucet_address`;

CREATE TABLE IF NOT EXISTS`faucet_address` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`network` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`platform` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`address` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`status` INT(11) NULL DEFAULT NULL COMMENT '0:init,20:success,21:coin_success,40:fail,41:coin_fail,42:coin_already_transfered',
	`url` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`amount` BIGINT(20) NULL DEFAULT NULL,
	`transfered_txn` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	`transfered_at` DATETIME NULL DEFAULT NULL,
	`created_at` DATETIME NULL DEFAULT NULL,
	`updated_at` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `ix_faucet_address` (`address`) USING BTREE,
	INDEX `ix_faucet_address_network_transfered_at_status` (`address`, `network`, `transfered_at`, `status`) USING BTREE,
	INDEX `ix_faucet_url_platform_created_at_status` (`url`, `platform`, `created_at`, `status`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

ALTER TABLE
    faucet_address 
ADD 
    COLUMN scrape_retry SMALLINT NOT NULL comment '';

ALTER TABLE
    faucet_address 
ADD 
    COLUMN transfer_retry SMALLINT NOT NULL comment '';