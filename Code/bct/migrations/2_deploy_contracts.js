const CollabFed = artifacts.require("UserRequestContract");
const ResourceResponse = artifacts.require("ResourceResponseContract");

module.exports = function (deployer) {
  deployer.deploy(CollabFed);
  deployer.deploy(ResourceResponse);
};
