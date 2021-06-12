<?php

class Compressor
{	
	const VERSION = "2.5.6";
	const VERSION_COMPATIBLE = "2.213"; // version of min compatible Pivot Component
	public static $TIME_ZONE = 'UTC';

	/**
	 * Compress MySql result
	 * @param input - MySql result
	 * @return boolean
	 */
	public static function compressMySql($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new MySqlReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress MySqli result
	 * @param input - MySqli result
	 * @return boolean
	 */
	public static function compressMySqli($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new MySqliReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress MS SQL Server result (Linux)
	 * @param input - MS SQL Server result
	 * @return boolean
	 */
	public static function compressMSSQL($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new MSSQLReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress MS SQL Server result
	 * @param input - MS SQL Server result
	 * @return boolean
	 */
	public static function compressSQLSRV($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new SQLSRVReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress PostgreSQL result
	 * @param input - PostgreSQL result
	 * @return boolean
	 */
	public static function compressPostgreSQL($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new PostgreSQLReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}
		
	/**
	 * Compress Oracle OCI result
	 * @param input - Oracle OCI result
	 * @return boolean
	 */
	public static function compressOCI($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new OCI8Reader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress PDO result
	 * @param input - PDOStatement object
	 * @return boolean
	 */
	public static function compressPDO($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new PDOReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress array of data
	 * @param input - array of data
	 * @return boolean
	 */
	public static function compressArray($input, $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new ArrayReader();
		$reader->outFile = $outFile;
		return $reader->process($input);
	}

	/**
	 * Compress CSV file with specified path
	 * @param filePath - path to file in CSV format
	 * @param delimiter - character used to separate the values. By default is comma or colon
	 * @return boolean
	 */
	public static function compressFile($filePath, $delimiter = "", $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$reader = new FileReader();
		$reader->delimiter = $delimiter;
		$reader->outFile = $outFile;
		return $reader->process($filePath);
	}

	/**
	 * Compress string data in CSV format
	 * @param input - string data in CSV format
	 * @param delimiter - character used to separate the values. By default is comma or colon
	 * @param recordsetDelimiter - character used to separate the rows. By default is caret return
	 * @return boolean
	 */
	public static function compressString($input, $delimiter = "", $recordsetDelimiter = "\n", $outFile = null) {
		if (ob_get_contents()) ob_end_clean();
		$input = explode($recordsetDelimiter, $input);
		return Compressor::compressArray($input, $delimiter, $outFile);
	}
}

/* Backward compatibility */
class CSVCompressor {
	public function compressFile($filePath, $delimiter = "") {
		return Compressor::compressFile($filePath, $delimiter);
	}
	public function compressDataString($input, $delimiter = "") {
		return Compressor::compressString($input, $delimiter);
	}
	public function compressDataMySql($input) {
		return Compressor::compressMySql($input);
	}
	// deprecated
	public function setMonthLabels($month) { }
	public function setQuarterLabels($quarter) { }
	public function compressDataStringArray($input, $delimiter = "") { }
}

abstract class BaseReader {
	protected $FIELD_DELIMITER = ",";
	protected $RECORDSET_DELIMITER = "\n";
	protected $header;
	private $_headerLength;
	private $TIME_ZONE;
	public $outFile;

	public function __construct () {
		$this->TIME_ZONE = new DateTimeZone(Compressor::$TIME_ZONE);
	}

	protected function addColumn($caption, $type) {
		$column = array(
			"caption" => $caption,
			"type" => $type,
			"members" = array()
		);
		if ($type == ColumnType::LEVELS) {
			$parent = explode(":", $caption)[0];
			$column["parentIdx"] = array_search($parent, array_column($this->header, "caption"));
		}
		$this->header[] = $column;
		$this->_headerLength = count($this->header);
	}

	protected function composeHeader() {
		$columns = array();
		for ($i = 0; $i < count($this->header); $i++){
			$column = $this->header[$i];
			$columns[$i] = $this->getColumnPrefix($column["type"]).$this->encodeChars($column["caption"]);
		}
		if ($this->outFile) {
			file_put_contents($this->outFile, "");
		}
		$this->out("___ocsv2___".Compressor::VERSION."/".Compressor::VERSION_COMPATIBLE."\n", true); // version
		$this->out(join(",", $columns)."\n");
	}

	protected function composeDataRow($values) {
		for ($colIdx = 0; $colIdx < $this->_headerLength; $colIdx++) {
			$value = isset($values[$colIdx]) ? $values[$colIdx] : "";
			$values[$colIdx] = $this->addMember($value, $colIdx);
		}
		$this->out(join(",", $values)."\n");
	}

	protected function addMember($value, $colIdx) {
		$type = $this->header[$colIdx]["type"];
		if ($type == ColumnType::FACT) {
			return $value;
		} elseif ($type == ColumnType::STRING
				|| $type == ColumnType::WEEKDAY
				|| $type == ColumnType::MONTH
				|| $type == ColumnType::LEVELS) {
			$_colIdx = (isset($this->header[$colIdx]["parentIdx"]) && $this->header[$colIdx]["parentIdx"] !== false) 
				? $this->header[$colIdx]["parentIdx"] : $colIdx;
			if (isset($this->header[$_colIdx]["members"][strtolower($value)])) {
				return $this->header[$_colIdx]["members"][strtolower($value)];
			} else {
				$this->header[$_colIdx]["members"][strtolower($value)] = "^".count($this->header[$_colIdx]["members"]);
				return $this->encodeChars($value);
			}
		} else if ( $type == ColumnType::DATE
				|| $type == ColumnType::DATE_STRING 
				|| $type == ColumnType::DATE_WITH_MONTHS
				|| $type == ColumnType::DATE_WITH_QUARTERS) {
			if ($value == "") return $value;
			$date = null;
			if ($value instanceof DateTime) {
				$date = $value;
			} else {
				try {
					$date = new DateTime($value, $this->TIME_ZONE);
				} catch (Exception $e) {
					return null;
				}
			}
			return $date->getTimestamp();

		}
		return $value;
	}

	protected $chars = array(",", "\"", "\n");
	protected $chars_encoded = array("%d%", "%q%", "%n%");
	protected function encodeChars($input) {
		return str_replace($this->chars, $this->chars_encoded, $input);
	}

	private $buffer = "";
	private $buffer_clear = false;
	protected function out($data, $clear = false) {
		$this->buffer .= $data;
		$this->buffer_clear = $this->buffer_clear || $clear;
		if (strlen($this->buffer) > 25000) {
			$this->flush();
		}
	}

	public function flush() {
		if (strlen($this->buffer) > 0) {
			if ($this->outFile) {
				file_put_contents($this->outFile, $this->buffer, $this->buffer_clear ? 0 : FILE_APPEND);
			} else {
				echo $this->buffer;
			}
			$this->buffer = "";
			$this->buffer_clear = false;
		}
	}

	protected function getColumnType($column, $value = ""){
		if (strpos($column,":")) {
			return ColumnType::LEVELS;
		} else if (substr($column, 0, 1) == "+") {
			return ColumnType::STRING;
		} else if (substr($column, 0, 2) == "d+") {
			return ColumnType::DATE;
		} else if (substr($column, 0, 2) == "D+") {
			return ColumnType::DATE_WITH_MONTHS;
		} else if (substr($column, 0, 3) == "D4+") {				
			return ColumnType::DATE_WITH_QUARTERS;
		} else if (substr($column, 0, 3) == "ds+") {
			return ColumnType::DATE_STRING;
		} else if (substr($column, 0, 1) == "-") {
			return ColumnType::FACT;
		} else if (substr($column, 0, 2) == "t+") {
			return ColumnType::TIME;
		} else if (substr($column, 0, 3) == "dt+") {
			return ColumnType::DATETIME;
		} else if (substr($column, 0, 2) == "m+") {
			return ColumnType::MONTH;
		} else if (substr($column, 0, 2) == "w+") {
			return ColumnType::WEEKDAY;
		} else if (substr($column, 0, 2) == "n+") {
			return ColumnType::FACT;
		} else if (CompressorUtils::isNan($value)) {
			$date_val = strtotime($value);
			if (strtotime($value)) {
				return ColumnType::DATE;
			} else {
				return ColumnType::STRING;
			}				
		} else if ($value == "") {
			return ColumnType::STRING;
		}
		return ColumnType::FACT;
	}
	
	protected function getColumnCaption($column) {	
		if (substr($column, 0, 1) == "+") {
			return substr($column, 1 , strlen($column));
		} else if (substr($column, 0, 2) == "d+") {
			return substr($column, 2 , strlen($column));
		} else if (substr($column, 0, 2) == "D+") {
			return substr($column, 2 , strlen($column));
		} else if (substr($column, 0, 3) == "D4+") {				
			return substr($column, 3 , strlen($column));
		} else if (substr($column, 0, 3) == "ds+") {
			return substr($column, 3 , strlen($column));
		} else if (substr($column, 0, 1) == "-") {
			return substr($column, 1 , strlen($column));
		} else if (substr($column, 0, 2) == "t+") {
			return substr($column, 2 , strlen($column));
		} else if (substr($column, 0, 3) == "dt+") {
			return substr($column, 3 , strlen($column));
		} else if (substr($column, 0, 2) == "m+") {
			return substr($column, 2 , strlen($column));
		} else if (substr($column, 0, 2) == "w+") {
			return substr($column, 2 , strlen($column));
		} else if (substr($column, 0, 2) == "n+") {
			return substr($column, 2 , strlen($column));
		}
		return $column;
	}

	protected function getColumnPrefix($type) {
		if ($type == ColumnType::FACT) {
			return "-";
		} elseif ($type == ColumnType::STRING) {
			return "+";
		} elseif ($type == ColumnType::DATE) {
			return "d+";
		} elseif ($type == ColumnType::DATE_WITH_MONTHS) {
			return "D+";
		} elseif ($type == ColumnType::DATE_WITH_QUARTERS) {
			return "D4+";
		} elseif ($type == ColumnType::DATE_STRING) {
			return "ds+";
		} elseif ($type == ColumnType::WEEKDAY) {
			return "w+";
		} elseif ($type == ColumnType::MONTH) {
			return "m+";
		} elseif ($type == ColumnType::TIME) {
			return "t+";
		} elseif ($type == ColumnType::DATETIME) {
			return "dt+";
		} elseif ($type == ColumnType::LEVELS) {
			return "+";
		} 
		return "";
	}
}

abstract class DBReader extends BaseReader {
	public function process($input) {
		try {
			$this->parseHeader($input);
			$this->parseDataRows($input);
			$this->flush();
		} catch (Exception $e) {
			return false;
		}
		return true;
	}

	protected function parseHeader($input) {
		$fields = $this->getNumFields($input);
		for ($i = 0; $i < $fields; $i++) {
			$name = $this->getFieldName($input, $i);
			$type = $this->getDbColumnType($this->getFieldType($input, $i));
			$caption = $this->getColumnCaption($name);
			$type = ($caption == $name) ? $type : $this->getColumnType($name);
			$this->addColumn($caption, $type);
		}
		$this->composeHeader();
	}

	protected function parseDataRows($input) {
		while ($values = $this->fetchRow($input)) {
			$this->composeDataRow($values);
		}
	}

	protected function getDbColumnType($value) {
		$value = strtolower($value);
		if ($value == "tinyint" ||
			$value == "smallint" ||
			$value == "mediumint" ||
			$value == "int" ||
			$value == "bigint" ||
			$value == "float" ||
			$value == "double" ||
			$value == "decimal" || 
			$value == "real" ||
			$value == "short" ||
			$value == "long" || 
			$value == "longlong" ||
			$value == "numeric" ||
			$value == "integer") {
			return ColumnType::FACT;
		} else if ($value == "string") {
			return ColumnType::STRING;
		} else if ($value == "date" || 
			$value == "datetime" ||
			$value == "timestamp" ) {
			return ColumnType::DATE;
		} else if ($value == "time") {
			return ColumnType::TIME;
		} 
		return ColumnType::STRING;
	}

	abstract protected function getNumFields($input);
	abstract protected function getFieldName($input, $colIdx);
	abstract protected function getFieldType($input, $colIdx);
	abstract protected function fetchRow($input);
}

abstract class CSVReader extends BaseReader {
	private $FIELD_ENCLOSURE_TOKEN = "\"";
	private $headerRow;

	public $delimiter;

	public function processRow($row) {
		if (!isset($this->headerRow)) {
			$this->headerRow = $row;
		} elseif (isset($this->headerRow) && !isset($this->header)) {
			$this->processHeaderRow($this->headerRow, $row);
			$this->processDataRow($row);
		} else {
			$this->processDataRow($row);
		}
	}

	private function processHeaderRow($headerStr, $rowStr) {
		$this->header = array();
		$this->delimiter = $this->chooseSeparator($headerStr);
		$pattern = "/^\s+|\s+$/";
		$headerItems = $this->splitRow($headerStr);
		$rowItems = $this->splitRow($rowStr);
		for ($i = 0; $i < count($headerItems); $i++){
			$column = preg_replace($pattern, "", $headerItems[$i]);
			$type = isset($rowItems[$i]) ? $this->getColumnType($column, $rowItems[$i]) : ColumnType::STRING;
			$caption = $this->getColumnCaption($column);
			$this->addColumn($caption, $type);	
		}
		$this->composeHeader();
	}

	private function processDataRow($rowStr) {
		$rowStr = trim($rowStr);
		if (strlen($rowStr) <= 0){
			return;	
		}
		$values = $this->splitRow($rowStr);
		$this->composeDataRow($values);
	}

	private function chooseSeparator($row){
		if ($this->delimiter && strlen($this->delimiter) > 0) {
			return $this->delimiter;
		}
		$commas = count(explode(",", $row));
		$semicoloms = count(explode(";", $row));
		return ($commas > $semicoloms) ? "," : ";";
	}

	private function splitRow($rowStr){
		if (!isset($rowStr)) return array();
		$pattern = "/^\s+|\s+$/";
		$value = "";
		$quoted = false;
		$prevQuote = false;
		$parsed = array();
		$rowStrlength = strlen($rowStr);
		for ($i = 0; $i < $rowStrlength; $i++){
			$char = $rowStr[$i];
			if (($i == $rowStrlength - 1) || ($char == $this->delimiter && !$quoted)){
				if ($i == $rowStrlength - 1) $value = $value.$char;
				$value = preg_replace($pattern, "", $value);
				if (strlen($value) > 0 && $value[0] == $this->FIELD_ENCLOSURE_TOKEN && $value[strlen($value) - 1] == $this->FIELD_ENCLOSURE_TOKEN){
					$value = substr($value, 1, strlen($value) - 2);
				}
				$prevQuote = false;
				$quoted = false;
				$parsed[count($parsed)] = $value;
				$value = "";
			} else {
				if ($char == $this->FIELD_ENCLOSURE_TOKEN){
					if (!$prevQuote) $value = $value.$char;
					$quoted = !$quoted;
					$prevQuote = true;
				} else {
					$value = $value.$char;
					$prevQuote = false;
				}
			}
		}
		return $parsed;
	}
}

class FileReader extends CSVReader {
	public function process($filePath, $delimiter = "") {
		try {
			$file = fopen($filePath, "r");
			while (!feof($file)) {
				$this->processRow(fgets($file));
			}	
			fclose($file);
			$this->flush();
		} catch (Exception $e) {
			return false;
		}
		return true;
	}
}

class MySqlReader extends DBReader {
	protected function getNumFields($input) {
		return mysql_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		return mysql_field_name($input, $colIdx);
	}
	protected function getFieldType($input, $colIdx) {
		return mysql_field_type($input, $colIdx);
	}
	protected function fetchRow($input) {
		return mysql_fetch_row($input);
	}
}

class MySqliReader extends DBReader {
	private $types_hash = array(
		1=>'tinyint',
		2=>'smallint',
		3=>'int',
		4=>'float',
		5=>'double',
		7=>'timestamp',
		8=>'bigint',
		9=>'mediumint',
		10=>'date',
		11=>'time',
		12=>'datetime',
		13=>'year',
		16=>'bit',
		//252 is currently mapped to all text and blob types (MySQL 5.0.51a)
		253=>'varchar',
		254=>'char',
		246=>'decimal'
	);

	protected function getNumFields($input) {
		return mysqli_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		$finfo = mysqli_fetch_field_direct($input, $colIdx);
		return $finfo->name;
	}
	protected function getFieldType($input, $colIdx) {
		$finfo = mysqli_fetch_field_direct($input, $colIdx);
		return $this->types_hash[$finfo->type];
	}
	protected function fetchRow($input) {
		return mysqli_fetch_row($input);
	}
}

class MSSQLReader extends DBReader {
	protected function getNumFields($input) {
		return mssql_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		return mssql_field_name ($input, $colIdx);
	}
	protected function getFieldType($input, $colIdx) {
		return mssql_field_type($input, $colIdx);
	}
	protected function fetchRow($input) {
		return mssql_fetch_row($input);
	}
}

class SQLSRVReader extends DBReader {
	protected function getNumFields($input) {
		return sqlsrv_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		$meta = sqlsrv_field_metadata($input);
		return $meta[$colIdx]["Name"];
	}
	protected function getFieldType($input, $colIdx) {
		$meta = sqlsrv_field_metadata($input);
		$type = $meta[$colIdx]["Type"];
		if ($type == -5) return "bigint";
		if ($type == -2) return "binary";
		if ($type == -7) return "bit";
		if ($type == 1) return "char";
		if ($type == 91) return "date";
		if ($type == 93) return "datetime";
		if ($type == -155) return "datetimeoffset";
		if ($type == 3) return "decimal";
		if ($type == 6) return "float";
		if ($type == 4) return "int";
		if ($type == -8) return "nchar";
		if ($type == -10) return "ntext";
		if ($type == 2) return "numeric";
		if ($type == -9) return "nvarchar";
		if ($type == 7) return "real";
		if ($type == 5) return "smallint";
		if ($type == -1) return "text";
		if ($type == -154) return "time";
		if ($type == -6) return "tinyint";
		return "varchar";
	}
	protected function fetchRow($input) {
		return sqlsrv_fetch_array($input, SQLSRV_FETCH_NUMERIC);
	}
}

class PostgreSQLReader extends DBReader {
	protected function getNumFields($input) {
		return pg_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		return pg_field_name($input, $colIdx);
	}
	protected function getFieldType($input, $colIdx) {
		return pg_field_type($input, $colIdx);
	}
	private $rowIdx = 0;
	private $numRows = 0;
	protected function fetchRow($input) {
		if ($this->rowIdx == 0) {
			$this->numRows = pg_num_rows($input); 
		}
		return $this->rowIdx < $this->numRows ? pg_fetch_row($input, $this->rowIdx++) : null;
	}
}

class OCI8Reader extends DBReader {
	protected function getNumFields($input) {
		return oci_num_fields($input);
	}
	protected function getFieldName($input, $colIdx) {
		return oci_field_name($input, $colIdx);
	}
	protected function getFieldType($input, $colIdx) {
		return oci_field_type($input, $colIdx);
	}
	protected function fetchRow($input) {
		return oci_fetch_row($input);
	}
}

class PDOReader extends DBReader {
	protected function getNumFields($input) {
		return $input->columnCount();
	}
	protected function getFieldName($input, $colIdx) {
		$meta = $input->getColumnMeta($colIdx);
		return $meta["name"];
	}
	protected function getFieldType($input, $colIdx) {
		$meta = $input->getColumnMeta($colIdx);
		return $meta["native_type"];
	}
	protected function fetchRow($input) {
		return $input->fetch(PDO::FETCH_NUM);
	}
}

class ArrayReader extends DBReader {
	public function process($input) {
		try {
			$length = count($input);
			$this->parseHeader($input[0]);
			for ($i=1; $i < $length; $i++) { 
				$this->composeDataRow($input[$i]);
			}
			$this->flush();
		} catch (Exception $e) {
			return false;
		}
		return true;
	}

	protected function parseHeader($input) {
		foreach ($input as $field) {
			$this->addColumn($field["name"], $this->getDbColumnType($field["type"]));
		}
		$this->composeHeader();
	}

	protected function getNumFields($input) { }
	protected function getFieldName($input, $colIdx) { }
	protected function getFieldType($input, $colIdx) { }
	protected function fetchRow($input) { }
}

abstract class ColumnType
{
	const FACT = 0;					// fact
	const STRING = 1;				// string
	const DATE = 2;					// imple date of 3 (Year|Month|Day)
	const LEVELS = 4;				// levels
	const DATE_WITH_MONTHS = 6;		// hierarchical date of 3 (Year|Month|Day)
	const MONTH = 10;				// month
	const DATE_WITH_QUARTERS = 11;	// hierarchical date of 4 (Year|Quarter|Month|Day)
	const TIME = 13;				// time measure (hh:mm:ss)
	const WEEKDAY = 14;				// weekday
	const DATETIME = 15;			// date/time measure (mm/dd/yyyy hh:mm:ss) 
	const DATE_STRING = 16;			// date string (mm/dd/yyyy)
}

class CompressorUtils
{
	public static function isNaN($value) {
		//Don't forget to mention we do not support all the types. Check, what to we need to support.
		$f_val = filter_var($value, FILTER_VALIDATE_FLOAT/*, array(FILTER_FLAG_ALLOW_THOUSAND, )*/);
		if ($f_val === FALSE) {
			return true;
		} else {
			return false;
		}
	}
}

?>
